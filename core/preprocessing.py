import pandas as pd
import logging
from core.singleton import SingletonMeta

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class DataPreprocessor:
    """
    Class to handle various preprocessing operations on a Pandas DataFrame.
    """

    def __init__(self, data):
        """
        Initialize the preprocessor with a dataset.

        :param data: pd.DataFrame - The dataset to preprocess.
        """
        logging.info("Initializing DataPreprocessor")
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a Pandas DataFrame.")
        self.original_data = data.copy()
        self.data = data

    def reset_data(self):
        """
        Reset the dataset to its original state.

        :return: None
        """
        self.data = self.original_data.copy()

    def handle_nulls(self, method="mean", fill_value=None):
        """
        Handle null values in the dataset.

        :param method: str - The method to handle nulls. Options: 'mean', 'drop', 'fill'.
        :param fill_value: Any - The value to use for filling nulls (if method is 'fill').
        :return: pd.DataFrame - Preprocessed DataFrame.
        """
        try:
            if method == "mean":
                self.data = self.data.fillna(self.data.mean(numeric_only=True))
            elif method == "drop":
                self.data = self.data.dropna()
            elif method == "fill":
                if fill_value is None:
                    raise ValueError(
                        "fill_value must be provided when method is 'fill'."
                    )
                self.data = self.data.fillna(fill_value)
            else:
                raise ValueError(
                    "Invalid method for handling nulls. Choose from 'mean', 'drop', or 'fill'."
                )
        except Exception as e:
            raise
        return self.data

    def rename_columns(self, column_mapping):
        """
        Rename columns in the dataset.

        :param column_mapping: dict - A dictionary mapping old column names to new column names.
        :return: pd.DataFrame - DataFrame with renamed columns.
        """
        if not isinstance(column_mapping, dict):
            raise ValueError("column_mapping must be a dictionary.")
        self.data = self.data.rename(columns=column_mapping)
        return self.data

    def drop_columns(self, columns_to_drop):
        """
        Drop specified columns from the dataset.

        :param columns_to_drop: list - A list of column names to drop.
        :return: pd.DataFrame - DataFrame with columns dropped.
        """
        if not isinstance(columns_to_drop, list):
            raise ValueError("columns_to_drop must be a list.")
        self.data = self.data.drop(columns=columns_to_drop, errors="ignore")
        return self.data

    def get_data(self):
        """
        Retrieve the preprocessed dataset.

        :return: pd.DataFrame - The preprocessed DataFrame.
        """
        return self.data
