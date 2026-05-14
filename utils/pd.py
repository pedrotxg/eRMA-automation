import pandas as pd


class PandasUtils:
    """
    Utility class with common functions for data manipulation using Pandas.
    """

    def __init__(self, dataframe: pd.DataFrame = None):
        self.df = dataframe

    # -------------------------
    # Load Data
    # -------------------------
    def load_csv(self, file_path: str, **kwargs):
        """Loads a CSV file."""
        self.df = pd.read_csv(file_path, **kwargs)
        return self.df

    def load_excel(self, file_path: str, **kwargs):
        """Loads an Excel file."""
        self.df = pd.read_excel(file_path, **kwargs)
        return self.df

    def load_json(self, file_path: str, **kwargs):
        """Loads a JSON file."""
        self.df = pd.read_json(file_path, **kwargs)
        return self.df

    # -------------------------
    # Save Data
    # -------------------------
    def save_csv(self, file_path: str, **kwargs):
        """Saves DataFrame to CSV."""
        self.df.to_csv(file_path, index=False, **kwargs)

    def save_excel(self, file_path: str, **kwargs):
        """Saves DataFrame to Excel."""
        self.df.to_excel(file_path, index=False, **kwargs)

    def save_json(self, file_path: str, **kwargs):
        """Saves DataFrame to JSON."""
        self.df.to_json(file_path, **kwargs)

    # -------------------------
    # Data Information
    # -------------------------
    def get_shape(self):
        """Returns DataFrame shape."""
        return self.df.shape

    def get_columns(self):
        """Returns column names."""
        return self.df.columns.tolist()

    def get_dtypes(self):
        """Returns column data types."""
        return self.df.dtypes

    def get_head(self, rows: int = 5):
        """Returns first rows."""
        return self.df.head(rows)

    def get_tail(self, rows: int = 5):
        """Returns last rows."""
        return self.df.tail(rows)

    def get_summary(self):
        """Returns statistical summary."""
        return self.df.describe()

    def get_null_count(self):
        """Returns null value count."""
        return self.df.isnull().sum()

    # -------------------------
    # Data Selection
    # -------------------------
    def select_columns(self, columns: list):
        """Selects specific columns."""
        return self.df[columns]

    def filter_rows(self, condition):
        """Filters rows based on condition."""
        return self.df[condition]

    def get_unique_values(self, column: str):
        """Returns unique values from a column."""
        return self.df[column].unique()

    # -------------------------
    # Data Cleaning
    # -------------------------
    def drop_nulls(self):
        """Removes null rows."""
        self.df = self.df.dropna()
        return self.df

    def fill_nulls(self, value):
        """Fills null values."""
        self.df = self.df.fillna(value)
        return self.df

    def drop_duplicates(self):
        """Removes duplicate rows."""
        self.df = self.df.drop_duplicates()
        return self.df

    def rename_columns(self, columns_map: dict):
        """Renames columns."""
        self.df = self.df.rename(columns=columns_map)
        return self.df

    # -------------------------
    # Data Manipulation
    # -------------------------
    def add_column(self, column_name: str, values):
        """Adds a new column."""
        self.df[column_name] = values
        return self.df

    def remove_column(self, column_name: str):
        """Removes a column."""
        self.df = self.df.drop(columns=[column_name])
        return self.df

    def sort_values(self, column: str, ascending: bool = True):
        """Sorts DataFrame by column."""
        self.df = self.df.sort_values(by=column, ascending=ascending)
        return self.df

    def group_by(self, columns, agg_func="mean"):
        """Groups DataFrame."""
        return self.df.groupby(columns).agg(agg_func)

    def merge_dataframe(self, other_df, on: str, how: str = "inner"):
        """Merges DataFrames."""
        self.df = pd.merge(self.df, other_df, on=on, how=how)
        return self.df

    # -------------------------
    # Index
    # -------------------------
    def reset_index(self):
        """Resets DataFrame index."""
        self.df = self.df.reset_index(drop=True)
        return self.df

    def set_index(self, column: str):
        """Sets DataFrame index."""
        self.df = self.df.set_index(column)
        return self.df

    # -------------------------
    # Copy
    # -------------------------
    def copy_dataframe(self):
        """Returns a copy of DataFrame."""
        return self.df.copy()

    # -------------------------
    # Value Access
    # -------------------------
    def get_value(self, row_index, column_name):
        """Gets a specific value."""
        return self.df.loc[row_index, column_name]

    def set_value(self, row_index, column_name, value):
        """Sets a specific value."""
        self.df.loc[row_index, column_name] = value
        return self.df
