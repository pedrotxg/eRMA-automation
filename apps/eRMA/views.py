from django.shortcuts import render
from django.http import JsonResponse

from apps.eRMA.flows.automation.navegation import *
from apps.eRMA.flows.automation.product import *

def get_data_from_serial_number(request, serial_number: str):
    session = SessionManager.instance()
    session.ensure_login()
    session.reset_page()

    product = Product()
    session.erma._product = product

    session.erma.search_serial_number(serial_number=serial_number)
    data = session.erma.get_product_information()

    return JsonResponse(data)
