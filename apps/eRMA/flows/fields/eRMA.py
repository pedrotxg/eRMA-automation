class LOGIN:
    ID_LOGIN_INPUT="#Username"
    ID_PASSWORD_INPUT="#Password"
    CLASS_NAME_BUTTON_LOGIN=".login-btn"

class WARRANTY_LOOKUP:
    ID_SEARCH_INPUT="#searchData"
    ID_SEARCH_BUTTON="#warranty_submit"
    WRONG_BARCODE_NO = {"seletor":".alertinfo", "texto": "Wrong Barcode No"}

class SERIAL_NUMBER_INFORMATION:
    class PRODUCT:
        SERIAL_NUMBER={"path":"label:text('Serial Number:')", "pos":0}
        PRODUCT_NAME={"path":"label:text('Product Name:')", "pos":0}
        BIOS_VERSION={"path":"label:text('BIOS Version:')", "pos":0}
        H_W_VERSION={"path":"label:text('H/W Version:')", "pos":0}

    class WARRANTY:
        SERIAL_NUMBER={"path":"label:text('Serial Number:')", "pos":1}
        PRODUCT_NAME={"path":"label:text('Product Name:')", "pos":1}
        SHIPPING_DATE={"path":"label:text('Shipping Date:')", "pos":0}
        H_W_VERSION={"path":"label:text('H/W Version:')", "pos":1}
        WARRANTY={"path":"label:text('Warranty:')", "pos":0}
        BIOS={"path":"label:text('BIOS:')", "pos":0}
        SALES_ORDER={"path":"label:text('Sales Order:')", "pos":0}
        CUSTOMER_NO={"path":"label:text('Customer No:')", "pos":0}
        M_O_DATE={"path":"label:text('M/O Date:')", "pos":0}
        M_O={"path":"label:text('M/O:')", "pos":0}
        CUST_S_N={"path":"label:text('Cust. S/N:')", "pos":0}
        CUST_P_N={"path":"label:text('Cust. P/N:')", "pos":0}

class PLM_ECO:
    ID_PART_NUMBER_INPUT="#PartNumber"
    ID_HW_INPUT="#REV"
    ID_BOARD_INPUT="#Board_CUT_IN"
    ID_SYSTEM_INPUT="#System_CUT_IN"
    ID_START_REALESE_DATE="#Start_DT"
    ID_END_REALESE_DATE="#End_DT"
    CLASS_BUTTON_SEARCH="button.btn.btn-primary"
    
    LOCATOR_RMA_TABLE="table.rma_table.top10 tbody tr"
...