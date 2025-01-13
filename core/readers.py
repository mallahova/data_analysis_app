"""
This module provides a factory for creating data readers based on file extension."""

import pandas as pd
from abc import ABC, abstractmethod
import io
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
    def get_reader(file):
        # Extract the file extension
        if isinstance(file, io.BytesIO):  # Check if file is a BytesIO object (Streamlit file uploader type)
            file_extension = file.name.split('.')[-1].lower()
            
            if file_extension == 'csv':
                return CSVReader()
            elif file_extension == 'json':
                return JSONReader()
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
        else:
            _, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower()

            if file_extension == '.csv':
                return CSVReader()
            elif file_extension == '.json':
                return JSONReader()
            else:
                raise ValueError(f"Unsupported file type: {file_extension}")
