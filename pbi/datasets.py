from numpy import float16, float32, float64
from numpy import int8, int16, int32, int64
from numpy import bool8
from powerbi.client import PowerBiClient
from powerbi.utils import Table, Column, Dataset, Relationship
from powerbi.enums import ColumnDataTypes
from pandas import DataFrame
import json

from datamgmt.dataframes import jsonifyDf
from pbi import config_info, credentials

def buildPowerBiClient() -> PowerBiClient:
    """
    """

    return PowerBiClient(
        client_id=config_info['client_id'],
        client_secret=config_info['client_secret'],
        redirect_uri=config_info['redirect_uri'],
        scope=['https://analysis.windows.net/powerbi/api/.default'],
        credentials=credentials
    )

def getDataTypes(df : DataFrame) -> dict:
    """
    """

    dataTypes = {}
    for col in df.columns:
        if df[col].dtype in [float16, float32, float64]:
            dataTypes[col] = ColumnDataTypes.Decimal
        elif df[col].dtype in [int8, int16, int32, int64]:
            dataTypes[col] = ColumnDataTypes.Int64
        elif df[col].dtype == bool8:
            dataTypes[col] = ColumnDataTypes.Boolean
        else:
            dataTypes[col] = ColumnDataTypes.String
    
    return dataTypes

def buildTable(df : DataFrame, tableName : str) -> Table:
    """
    """

    dataTypes = getDataTypes(df)
    table = Table(tableName)

    for col in df.columns:
        table.add_column(column=Column(name=col, data_type=dataTypes[col]))

    return table

def buildDataset(dfs : dict, datasetName : str, relationships : dict) -> Dataset:
    """
    """

    dataset = Dataset(name=datasetName)
    dataset.default_mode = 'Push'

    for name, df in dfs.items():
        table = buildTable(df, name)
        table.add_row(json.loads(jsonifyDf(df)))
        dataset.add_table(table=table)

    if relationships is not None:
        #relationships = setUpRelationships(dfs)
        print(relationships)
        buildRelationships(relationships, dataset)

    return dataset

def setUpRelationships(dfs : dict) -> dict:
    """
    """

    relationships = None
    for name, df in dfs.items():
        if relationships is None:
            relationships = {}
            for col in df.columns:
                relationships[col] = [name]
        else:
            for col in df.columns:
                if col in relationships.keys():
                    relationships[col].append(name)
                else:
                    relationships[col] = [name]

    killCols = []
    for col, tables in relationships.items():
        if len(tables) == 1:
            killCols.append(col)

    customTest = ['cost_ctr', 'tenure_id']
    for customCol in customTest:
        killCols.append(customCol)
    
    for col in killCols:
        del relationships[col]

    return relationships

def getColumnFromTable(table : Table, columnName : str) -> Column:
    """
    """

    for column in table.columns:
        if column.name == columnName:
            return Column

def buildRelationships(relationships : dict, dataset : Dataset, counter : int = 0) -> Dataset:
    """
    """

    for col, tables in relationships.items():
        if len(tables) == 2:
            table1 = tables[0]
            table2 = tables[1]
            
            relationship = Relationship(name=str(counter), from_table=table1, to_table=table2, from_column=col, to_column=col)
            relationship.cross_filtering_behavior = 'BothDirections'
            dataset.add_relationship(relationship=relationship)
            counter += 1
        else:
            table1 = tables[0]

            for table in tables[1:]:
                table2 = table
                
                relationship = Relationship(name=str(counter), from_table=table1, to_table=table2, from_column=col, to_column=col)
                relationship.cross_filtering_behavior = 'BothDirections'
                dataset.add_relationship(relationship=relationship)
                counter += 1

    return dataset

def pushToPowerBi(dfs : dict, datasetName : str, relationships : bool = False) -> None:
    """
    """

    dataset = buildDataset(dfs=dfs, datasetName=datasetName, relationships=relationships)
    group_id = config_info['group_id']

    client = buildPowerBiClient()
    service = client.push_datasets()

    service.post_group_dataset(group_id=group_id, dataset=dataset)
