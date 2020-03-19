import os

import openpyxl

from handlers.handler import Handler

class ExcelHandler(Handler):
    
    def __init__(self):
        
        self._workbook: openpyxl.Workbook = None
    
    
    def run(self, *args, **kwargs) -> openpyxl.Workbook:
        
        if kwargs is None:
            print(__name__,'::run() invalid supplied parameters, ', kwargs)
            return None
        
        file_name: str = kwargs.get('file_name')
        sheet_name: str = kwargs.get('name')
        
        if file_name is None:
            print(__name__,'::run() invalid supplied file_name, ', kwargs)
            return None
        
        if self._workbook is None:
            
            if os.path.isfile(file_name):
                self._workbook = openpyxl.load_workbook(filename=file_name)
            else
                self._workbook = openpyxl.Workbook()
            
            if self._workbook is None:
                print(__name__,'::run() could not open ', file_name)
                return None
                
            wb: openpyxl.Workbook = self._workbook
            ws = wb.activate if file_name is None else wb[file_name]
            print('Sheet name:', file_name)
            ws.write_rows()
            
        return file_name
        