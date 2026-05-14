class Product:
    def __init__(self):
        self._serial_number=None
        self._part_number=None
        self._max_realease_date=None

        self._valid_serial_number=None
        self._serial_number_data=None
        self._part_number_data_with_R_or_C=None
        self._part_number_data=None

        self._contains_R=False
        self._contains_C=False
        
        self._success=None

    def _clear_data(self):
        self._serial_number=None
        self._part_number=None
        self._max_realease_date=None

        self._serial_number_data=None
        self._part_number_data_with_R_or_C=None
        self._part_number_data=None

        self._contains_R=False
        self._contains_C=False
        
        self._success=None