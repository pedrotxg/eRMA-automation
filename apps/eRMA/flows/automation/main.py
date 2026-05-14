import os
import sys
sys.path.insert(0,"")
import pandas as pd

from apps.eRMA.flows.utils.utils import import_files, export_files, format_values_for_return

from apps.eRMA.flows.automation import navegation
from apps.eRMA.flows.automation.product import Product

PATH_FILE=os.getenv('PATH_FILE')
PATH_SAVE=os.getenv('PATH_SAVE')
HEADLESS=os.getenv('HEADLESS')

if __name__ == "__main__":
    nav = navegation.Navegador(headless=True if HEADLESS == "True" else False)
    product = Product()

    base_sn = import_files(PATH_FILE)
    base_sn["Contains_C"] = pd.NA
    base_sn["Contains_R"] = pd.NA
    base_sn["DateMaxSearch"] = pd.NA

    for i, product_data in enumerate(base_sn.values):
        print(f"Consult line: {i+1}")
        try:
            nav.reset_page()
            erma = navegation.SystemERMA(page=nav.page, product=product)
            erma.login()

            # Consult serial number
            erma.search_serial_number(serial_number=product_data[1])

            # Invalid serial number consult
            if not product._valid_serial_number:
                base_sn.loc[i, "Success"] = 0
                base_sn.loc[i, "Contains_C"] = "INVALID_SERIAL_NUMBER"
                base_sn.loc[i, "Contains_R"] = "INVALID_SERIAL_NUMBER"
                base_sn.loc[i, "DateMaxSearch"] = "INVALID_SERIAL_NUMBER"
                export_files(df=base_sn, path=PATH_SAVE)
                product._clear_data()
                continue

            # Get data from serial number
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

        except Exception as e:
            base_sn.loc[i, "Success"] = 0
            base_sn.loc[i, "Contains_C"] = "EXECUTION_ERROR"
            base_sn.loc[i, "Contains_R"] = "EXECUTION_ERROR"
            base_sn.loc[i, "DateMaxSearch"] = str(e)

            export_files(df=base_sn, path=PATH_SAVE)
            product._clear_data()

        # Save datas
        export_files(df=base_sn, path=PATH_SAVE)
        product._clear_data()

    ...