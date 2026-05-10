from playwright.sync_api import Page, sync_playwright
from datetime import datetime
from dotenv import load_dotenv
from time import sleep

import os
import sys
sys.path.insert(0,"")
load_dotenv()

from apps.eRMA.flows.automation.product import Product
from apps.eRMA.flows.utils.pw import PlaywrightUtils
from apps.eRMA.flows.fields import eRMA


class Navegador:
    def __init__(self, headless:bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def new_page(self) -> Page:
        return self.browser.new_page()
    
    def close_page(self) -> None:
        self.browser.close()
    
    def close(self) -> None:
        self.browser.close()
        self.playwright.stop()
        
    def reset_page(self) -> Page:
        if self.page:
            self.page.close()

        self.page = self.browser.new_page()
        return self.page

class SystemERMA:
    def __init__(self, page:Page, product:Product = Product()):
        self.page = page
        self.pw = PlaywrightUtils(page=self.page)

        # Check's
        self._logged=False
        self._page_consulted=None
        self._serial_number_consulted=False
        self._part_number_consulted=False

        # Product
        self._product=product

    def login(self) -> None:
        self.page.goto(os.getenv("LOGIN_URL"))
        self.pw.wait_load()

        self.pw.fill(seletor=eRMA.LOGIN.ID_LOGIN_INPUT, texto=os.getenv("USER_LOGIN"))
        self.pw.fill(seletor=eRMA.LOGIN.ID_PASSWORD_INPUT, texto=os.getenv("USER_PASSWORD"))
        self.pw.click(seletor=eRMA.LOGIN.CLASS_NAME_BUTTON_LOGIN)
        self.pw.wait_load()

        self.page.context.storage_state(path="auth.json")

        self._logged=True
        self._page_consulted="Login"
    
    def search_serial_number(self, serial_number:str) -> None:
        self.page.goto(os.getenv("SEARCH_SERIAL_NUMBER"))
        self.pw.wait_load()

        self.pw.fill(seletor=eRMA.WARRANTY_LOOKUP.ID_SEARCH_INPUT, texto=serial_number)
        self.pw.click(seletor=eRMA.WARRANTY_LOOKUP.ID_SEARCH_BUTTON)
        self.pw.wait_load()

        self._serial_number_consulted=True
        self._page_consulted="Search Serial Number"

        self._product._serial_number=serial_number

    def get_product_information(self, serial_number:str = None) -> dict[str]:
        if not self._serial_number_consulted:
            if serial_number:
                self._product._serial_number= serial_number

            if self._product._serial_number:
                self.search_serial_number(serial_number=self._product._serial_number)
            else:
                raise RuntimeError("Cannot proceed without a Serial Number.")

        part_number=self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.PRODUCT_NAME["path"],pos=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.PRODUCT_NAME["pos"], parent_element=True).split(":")[1].strip()
        max_realease_date = self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.M_O_DATE["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.M_O_DATE["pos"], parent_element=True).split(":")[1].strip()

        serial_number_data = {
            "product_information": {
                "serial_number":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.SERIAL_NUMBER["path"],pos=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.SERIAL_NUMBER["pos"], parent_element=True).split(":")[1].strip(),
                "product_name":part_number,
                "bios_version":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.BIOS_VERSION["path"],pos=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.BIOS_VERSION["pos"], parent_element=True).split(":")[1].strip(),
                "hw_verion":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.H_W_VERSION["path"],pos=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.H_W_VERSION["pos"], parent_element=True).split(":")[1].strip(),
            },
            "warranty_information": {
                "serial_number":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.SERIAL_NUMBER["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.SERIAL_NUMBER["pos"], parent_element=True).split(":")[1].strip(),
                "product_name":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.PRODUCT_NAME["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.PRODUCT_NAME["pos"], parent_element=True).split(":")[1].strip(),
                "shipping_date":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.SHIPPING_DATE["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.SHIPPING_DATE["pos"], parent_element=True).split(":")[1].strip(),
                "hw_verion":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.H_W_VERSION["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.H_W_VERSION["pos"], parent_element=True).split(":")[1].strip(),
                "warranty":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.WARRANTY["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.WARRANTY["pos"], parent_element=True).split(":")[1].strip(),
                "bios":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.BIOS["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.BIOS["pos"], parent_element=True).split(":")[1].strip(),
                "sales_order":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.SALES_ORDER["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.SALES_ORDER["pos"], parent_element=True).split(":")[1].strip(),
                "customet_no":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.CUSTOMER_NO["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.CUSTOMER_NO["pos"], parent_element=True).split(":")[1].strip(),
                "mo_date":max_realease_date,
                "mo":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.M_O["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.M_O["pos"], parent_element=True).split(":")[1].strip(),
                "cust_sn":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.CUST_S_N["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.CUST_S_N["pos"], parent_element=True).split(":")[1].strip(),
                "cust_pn":self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.CUST_P_N["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.CUST_P_N["pos"], parent_element=True).split(":")[1].strip(),
            }
        }

        self._page_consulted="Warranty Lookup"

        self._product._part_number=part_number
        self._product._serial_number_data=serial_number_data
        self._product._max_realease_date=datetime.strptime(max_realease_date,"%m/%d/%Y")

        return serial_number_data

    def get_product_name(self):
        ...

    def get_mo_date(self):
       ...

    def search_part_number(self, part_number:str = None, max_realease_date:datetime = None) -> None:
        if not self._product._part_number:
            if part_number:
                self._product._part_number=part_number
            else:
                raise RuntimeError("Cannot proceed without a Part Number.")

        if not self._product._max_realease_date:
            if max_realease_date:
                self._product._max_realease_date=max_realease_date
            else:
                raise RuntimeError("Cannot proceed without a Realese Date.")

        self.page.goto(os.getenv("SEARCH_PART_NUMBER"))
        self.pw.wait_load()

        self.pw.fill(seletor=eRMA.PLM_ECO.ID_PART_NUMBER_INPUT, texto=self._product._part_number)
        self.pw.fill(seletor=eRMA.PLM_ECO.ID_START_REALESE_DATE, texto=datetime.strftime(self._product._max_realease_date,"%Y-%m-%d"))
        sleep(0.2)

        self.pw.click(seletor=eRMA.PLM_ECO.CLASS_BUTTON_SEARCH)
        self.pw.wait_load()

        self._part_number_consulted=True
        self._page_consulted="PLM ECO"

    def get_part_number_datas(self, part_number:str = None, max_realease_date:datetime = None):
        if not self._part_number_consulted:
            if not self._product._part_number:
                if part_number:
                    self._product._part_number=part_number

            if not self._product._max_realease_date:
                if max_realease_date:
                    self._product._max_realease_date=max_realease_date

            if self._product._part_number and self._product._max_realease_date:
                self.search_part_number(part_number=self._product._part_number, max_realease_date=self._product._max_realease_date)
            else:
                raise RuntimeError("Cannot proceed without a Search Part Number in PLM ECO.")

        rows = self.pw.get_locator(eRMA.PLM_ECO.LOCATOR_RMA_TABLE)
        part_number_data = []
        part_number_data_with_R_or_C=[]

        for i in range(1, rows.count()):
            row = rows.nth(i)
            texts = row.locator("td").all_inner_texts()

            if len(texts) >= 8:
                part_number_data.append({
                    "id": texts[0].strip(),
                    "part_number": texts[1].strip(),
                    "hw": texts[2].strip(),
                    "eco": texts[3].strip(),
                    "status": texts[4].strip(),
                    "cut_in_board": texts[5].strip(),
                    "cut_in_system": texts[6].strip(),
                    "release_date": texts[7].strip(),
                })

        for line in part_number_data:
            self.verify_R_or_C_in_text(line['cut_in_board'])
            self.verify_R_or_C_in_text(line['cut_in_system'])
            
            if self._product._contains_R or self._product._contains_C:
                part_number_data_with_R_or_C.append(texts)

        return_part_number = {
            "contains_R_or_C": True if self._product._contains_R or self._product._contains_C else False,
            "part_number_data_with_R_or_C": part_number_data_with_R_or_C,
        }

        self._product._part_number_data=return_part_number
        self._product._part_number_data_with_R_or_C=part_number_data_with_R_or_C

        return return_part_number

    def verify_R_or_C_in_text(self, text:str) -> None:
        if '(R)' in text:
            self._product._contains_R=True

        elif'(C)' in text:
            self._product._contains_C=True

#

class Nav:
    def __init__(self, headless=True):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def reset_page(self):
        if self.page:
            self.page.close()

        self.page = self.context.new_page()
        return self.page

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

class SessionManager:
    _instance = None

    def __init__(self):
        self.nav = Navegador(headless=True)
        self.erma = SystemERMA(page=self.nav.page)
        self.login()

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()

        return cls._instance

    def login(self):
        self.erma.page = self.nav.page
        self.erma.login()

    def is_logged(self):
        try:
            return "login" not in self.nav.page.url.lower()

        except:
            return False

    def ensure_login(self):
        if not self.is_logged():
            self.nav.reset_page()
            self.erma.page = self.nav.page
            self.login()

    def reset_page(self):
        self.nav.reset_page()
        self.erma.page = self.nav.page
        self.erma.pw = PlaywrightUtils(page=self.nav.page)


if __name__ == "__main__":
    import time
    inicio = time.time()

    nav = Navegador(headless=True)
    product = Product()

    erma = SystemERMA(page=nav.page, product=product)
    erma.login()

    erma.search_serial_number(serial_number=os.getenv('SERIAL_NUMBER'))
    erma.get_product_information()
    
    fim = time.time()
    tempo_execucao = fim - inicio
    print(f"Tempo de execução: {tempo_execucao:.2f} segundos")
    ...