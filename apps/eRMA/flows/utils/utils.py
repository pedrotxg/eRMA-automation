from pandas import DataFrame
from datetime import datetime

from apps.eRMA.flows.utils.pd import PandasUtils
from apps.eRMA.flows.automation.product import Product


def import_files(path: str):
    df_utils = PandasUtils()
    df_utils.load_excel(path)

    return df_utils.df

def export_files(df: DataFrame, path: str):
    df_utils = PandasUtils(df)
    df_utils.save_excel(path)

def format_values_for_return(df:Product):
        return {
            "Contains_C": 1 if df._contains_C else 0,
            "Contains_R": 1 if df._contains_R else 0,
            "DateMaxSearch": datetime.strftime(df._max_realease_date, "%d/%m/%Y")
        }