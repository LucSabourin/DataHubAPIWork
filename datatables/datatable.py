from abc import abstractmethod, ABC


class DataTable(ABC):
    """
    Abstract class outlining what every concrete DataTable class must implement.
    """

    def __init__(self):
        pass

    def ingest(self):
        """Processes the data source into a pandas dataframe, so that to_json() can be called to
        retrieve the provisioned data.
        """
        self.create_meta_data()
        self.create_pandas_dataframe()
        self.clean_up()

    @abstractmethod
    def to_json(self) -> str:
        """Returns the json representation of the pandas dataframe"""
        pass

    @abstractmethod
    def create_meta_data(self):
        """Builds the required metadata for the source so a pandas dataframe can be created from it."""
        pass

    @abstractmethod
    def create_pandas_dataframe(self):
        """Creates a pandas dataframe from the source's data and metadata."""
        pass

    @abstractmethod
    def clean_up(self):
        """Performs any required housekeeping after creating the pandas dataframe"""
        pass
