# Pandas
import pandas as pd

# DataTable abstraction
from datatables.datatable import DataTable

# Excel File Scanning
from datatables.xl_workbook import XLWorkbook
from datatables.xl_worksheet import XLWorksheet

# Messages
from messages import Messages

# Data Management
from datamgmt.dataframes import jsonifyDf

class XLDataTable(DataTable):
    """
    Concrete DataTable implementation for an Excel worksheet.

    Converts an Excel Worksheet to a pandas dataframe and exposes that dataframe as JSON.
    """

    message_templates = {
        'could_not_load_into_pandas': ('The data from worksheet {0} could not be loaded into pandas for analysis.', 99),
        'empty_row': ('There is an empty row at index {1} in worksheet {0}.', 0),
        'empty_column': ('There is an empty column in field {1} of worksheet {0}.', 0),
    }

    def __init__(self, source: XLWorkbook, table: XLWorksheet, remove_empty: bool = False):
        self.source = source
        self.table = table
        self.remove_empty = remove_empty
        self.data_frame = None
        self.messages = Messages(XLDataTable.message_templates)

    def _build_pandas_schema(self):
        """
        Creates a schema dictionary that describes to pandas what worksheet in the Excel workbook
        to load into the dataframe.
        """
        schema = {
            'io': self.source.binary,
            'sheet_name': self.table.metadata['name'],
            'names': self.table.metadata['headers'],
        }

        # Skip rows above data (hierarchical fields and field headers) included in if/else statement above
        if 'field_header_row' in self.table.metadata.keys():
            schema['skiprows'] = range(self.table.metadata['field_header_row'] - 1)
        elif self.table.metadata['first_row'] > 1:
            schema['skiprows'] = range(self.table.metadata['first_row'] - 1)

        # Use columns containing data
        schema['usecols'] = range(
            self.table.metadata['first_column'] - 1,
            self.table.metadata['last_column']
        )

        return schema

    def create_meta_data(self):
        """
        Creates any metadata needed to load the raw data into the pandas dataframe.
        """
        # Required metadata has been created already by the XLWorksheet class.
        # self.table.metadata exposes this metadata.
        # But this may not be the case with all data sources.
        pass

    def create_pandas_dataframe(self):
        """
        Creates a pandas dataframe from our metadata and raw data.
        """
        schema = self._build_pandas_schema()
        try:
            self.data_frame = pd.read_excel(**schema)
        except:
            # We are intentionally absorbing the exception, so that we can report the message and
            # keep executing.
            self.messages.add_message('could_not_load_into_pandas', self.table.metadata['name'])

    def clean_up(self):
        """
        Adds error messages for empty rows or columns, and removes them from the dataframe.
        """
        df = self.data_frame

        # Columns
        for column_index, column in enumerate(df.columns):
            if df[df.columns[column_index]].count() == 0:
                self.messages.add_message(
                    'empty_column',
                    self.table.metadata['name'],
                    column
                )

        # Rows
        for row_index, row in df.iterrows():
            if row.isnull().all():
                self.messages.add_message(
                    'empty_row',
                    self.table.metadata['name'],
                    row_index
                )

        if self.remove_empty is True:
            df.dropna(how='all', inplace=True)

    def to_json(self) -> str:
        """
        Returns the json representation of the panda dataframe.
        """
        return jsonifyDf(self.data_frame)

