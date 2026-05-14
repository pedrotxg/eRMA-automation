import sys
sys.path.insert(0,"")
import pandas as pd

from utils.utils import import_files, export_files, format_values_for_return

from automation import navegation
from automation.product import Product

if __name__ == "__main__":
    nav = navegation.Navegador(headless=False)
    product = Product()

    base_sn = import_files("C:\\0 - Desenvolvimento\\auto-advantech\\0007552874.xlsx")
    base_sn["Contains_C"] = pd.NA
    base_sn["Contains_R"] = pd.NA
    base_sn["DateMaxSearch"] = pd.NA

    for i, product_data in enumerate(base_sn.values):
        print(f"Consult line: {i+1}")
        nav.reset_page()
        erma = navegation.SystemERMA(page=nav.page, product=product)
        erma.login()

        # Consult serial number
        erma.search_serial_number(serial_number=product_data[1])
        erma.get_product_information()

        # Consult part number
        erma.search_part_number()
        erma.get_part_number_datas()

        # Format data
        result = format_values_for_return(erma._product)
        for key, value in result.items():
            base_sn.loc[i, key] = value

        # Clear product for the next consult
        product._clear_data()

        # Just testing
        export_files(
            df=base_sn,
            path="C:\\0 - Desenvolvimento\\auto-advantech\\retorno.xlsx"
        )

    ...