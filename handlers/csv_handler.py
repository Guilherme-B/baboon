from csv import writer
from typing import Tuple

from handlers.handler import Handler

class CSVHandler(Handler):
    
    def __init__(self):
        pass
    
    def run(self, *args, **kwargs) -> Tuple:

        file_name: str = kwargs.get('file_name')
        
        if file_name is None:
            print(__name__,'::run() no file_name has been provided, ', options)
            return kwargs
        
        # Todo: Create a single reader as this might be terribly slow
        with open(file_name, 'a', newline='') as csv_file:
            csv_writer = writer(csv_file, delimiter=',', dialect='excel')

            csv_writer.writerow(list(*args))
            
        