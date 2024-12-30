import pandas as pd
from abc import ABC, abstractmethod
import os



class DataReader(ABC):
    """Abstract base class for all data readers."""
    @abstractmethod
    def read(self, source, **kwargs):
        pass


class CSVReader(DataReader):
    """Reader for CSV files."""
    def read(self, source, chunksize=None, delimiter=','):
        if chunksize:
            return pd.read_csv(source, chunksize=chunksize, delimiter=delimiter)
        return pd.read_csv(source, delimiter=delimiter)


class JSONReader(DataReader):
    """Reader for JSON files."""
    def read(self, source, orient='records'):
        return pd.read_json(source, orient=orient)


class FileReaderFactory:
    """Factory for creating appropriate data readers based on file extension."""
    @staticmethod
    def get_reader(file_name):
        # Extract the file extension
        _, file_extension = os.path.splitext(file_name)
        file_extension = file_extension.lower()

        if file_extension == '.csv':
            return CSVReader()
        elif file_extension == '.json':
            return JSONReader()
        else:
            raise ValueError(f"Unsupported file type: {file_extension}")


factory = FileReaderFactory()
reader = factory.get_reader('data_analysis_app/samples/Starbucks.csv')
data = reader.read('data_analysis_app/samples/Starbucks.csv', delimiter=',')
print(data.head())