import pandas as pd

class DataPreprocessor:
    """
    Class to handle various preprocessing operations on a Pandas DataFrame.
    """

    def __init__(self, data):
        """
        Initialize the preprocessor with a dataset.

        :param data: pd.DataFrame - The dataset to preprocess.
        """
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Input data must be a Pandas DataFrame.")
        self.original_data = data.copy()  # Preserve a copy of the original data
        self.data = data.copy()  # Work on a copy of the original data

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
        if method == "mean":
            self.data = self.data.fillna(self.data.mean(numeric_only=True))
        elif method == "drop":
            self.data = self.data.dropna()
        elif method == "fill":
            if fill_value is None:
                raise ValueError("fill_value must be provided when method is 'fill'.")
            self.data = self.data.fillna(fill_value)
        else:
            raise ValueError("Invalid method for handling nulls. Choose from 'mean', 'drop', or 'fill'.")
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

# Example usage
if __name__ == "__main__":
    # Example dataset
    sample_data = {
        "Name": ["Alice", "Bob", "Charlie", None],
        "Age": [25, 30, None, 22],
        "City": ["New York", None, "Los Angeles", "Chicago"],
    }
    df = pd.DataFrame(sample_data)

    # Initialize preprocessor
    preprocessor = DataPreprocessor(df)

    # Handle null values
    print("Original Data:")
    print(df)
    preprocessor.handle_nulls(method="fill", fill_value="Unknown")

    # Rename columns
    preprocessor.rename_columns({"Name": "Full Name", "City": "Location"})

    # Drop columns
    preprocessor.drop_columns(["Age"])

    # Reset data to original state
   #  preprocessor.reset_data()

    # Get the preprocessed data
    processed_data = preprocessor.get_data()
    print("\nPreprocessed Data:")
    print(processed_data)
