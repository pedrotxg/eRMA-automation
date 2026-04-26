from playwright.sync_api import Page, sync_playwright
from datetime import datetime

import os
import sys
sys.path.insert(0,"")
from utils.pw import PlaywrightUtils
from fields import eRMA


class Navegador:
    def __init__(self, headless:bool = False):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.page = self.browser.new_page()

    def new_page(self) -> Page:
        return self.browser.new_page()
    
    def close(self) -> None:
        self.browser.close()
        self.playwright.stop()

class SystemERMA:
    def __init__(self, page:Page):
        self.page = page
        self.pw = PlaywrightUtils(page=self.page)

        # Check's
        self._logged=False
        self._page_consulted=None
        self._serial_number_consulted=False
        self._part_number_consulted=False

        # Data
        self._serial_number=None
        self._part_number=None
        self._max_realease_date=None
        

    def login(self) -> None:
        self.page.goto(os.getenv("LOGIN_URL"))
        self.pw.wait_load()

        self.pw.fill(seletor=eRMA.LOGIN.ID_LOGIN_INPUT, texto=os.getenv("USER_LOGIN"))
        self.pw.fill(seletor=eRMA.LOGIN.ID_PASSWORD_INPUT, texto=os.getenv("USER_PASSWORD"))
        self.pw.click(seletor=eRMA.LOGIN.CLASS_NAME_BUTTON_LOGIN)
        self.pw.wait_load()

        self._page_consulted="Login"
        self._logged=True
    
    def search_serial_number(self, serial_number:str) -> None:
        self.page.goto(os.getenv("SEARCH_SERIAL_NUMBER"))
        self.pw.wait_load()

        self.pw.fill(seletor=eRMA.WARRANTY_LOOKUP.ID_SEARCH_INPUT, texto=serial_number)
        self.pw.click(seletor=eRMA.WARRANTY_LOOKUP.ID_SEARCH_BUTTON)
        self.pw.wait_load()

        self._page_consulted="Search Serial Number"
        self._serial_number=serial_number
        self._serial_number_consulted=True

    def get_product_information(self, serial_number:str = None) -> dict[str]:
        if not self._serial_number_consulted:
            if serial_number:
                self._serial_number= serial_number

            if self._serial_number:
                self.search_serial_number(serial_number=self._serial_number)
            else:
                raise RuntimeError("Cannot proceed without a Serial Number.")

        part_number=self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.PRODUCT_NAME["path"],pos=eRMA.SERIAL_NUMBER_INFORMATION.PRODUCT.PRODUCT_NAME["pos"], parent_element=True).split(":")[1].strip()
        max_realease_date = self.pw.get_text_by_pos(seletor=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.M_O_DATE["path"], pos=eRMA.SERIAL_NUMBER_INFORMATION.WARRANTY.M_O_DATE["pos"], parent_element=True).split(":")[1].strip()

        self._page_consulted="Warranty Lookup"
        self._part_number=part_number
        self._max_realease_date=datetime.strptime(max_realease_date,"%m/%d/%Y")

        return{
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

    def search_part_number(self, part_number:str = None, max_realease_date:datetime = None) -> None:
        if not self._part_number:
            if part_number:
                self._part_number=part_number
            else:
                raise RuntimeError("Cannot proceed without a Part Number.")

        if not self._max_realease_date:
            if max_realease_date:
                self._max_realease_date=max_realease_date
            else:
                raise RuntimeError("Cannot proceed without a Realese Date.")

        self.page.goto(os.getenv("SEARCH_PART_NUMBER"))
        self.pw.wait_load()

        self.pw.fill(seletor=eRMA.PLM_ECO.ID_PART_NUMBER_INPUT, texto=self._part_number)
        self.pw.fill(seletor=eRMA.PLM_ECO.ID_START_REALESE_DATE, texto=datetime.strftime(self._max_realease_date, "%Y-%m-%d"))
        self.pw.click(seletor=eRMA.PLM_ECO.CLASS_BUTTON_SEARCH)
        self.pw.wait_load()

        self._page_consulted="PLM ECO"
        self._part_number=part_number
        self._part_number_consulted=True

    def get_part_number_datas(self, part_number:str = None, max_realease_date:datetime = None):
        if not self._part_number_consulted:
            if not self._part_number:
                if part_number:
                    self._part_number=part_number

            if not self._max_realease_date:
                if max_realease_date:
                    self._max_realease_date=max_realease_date

            if self._part_number and self._max_realease_date:
                self.search_part_number(part_number=self._part_number, max_realease_date=self._max_realease_date)
            else:
                raise RuntimeError("Cannot proceed without a Search Part Number in PLM ECO.")

        ...


if __name__ == "__main__":
    nav = Navegador(headless=False)
    erma = SystemERMA(page=nav.page)
    erma.login()
    erma.search_serial_number(serial_number=os.getenv("SERIAL_NUMBER"))
    serial_number_data = erma.get_product_information()
    erma.search_part_number()
    ...