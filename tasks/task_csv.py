from tasks.task import Task
from handlers.csv_handler import CSVHandler

class TaskCsv(Task):
    
    _file_name:str = None
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._file_name = kwargs.get('file_name')
        
        self._handler = CSVHandler()
        
    def validate(self):
        file_name: str = self._file_name
        file_extension: str = '.csv'
        
        return file_name is not None and \
            len(file_name) > len(file_extension) and \
            file_name[-4:] == file_extension
        
    def run(self, *args, **kwargs):

        if self._handler is None:
            print(__name___, '::run() failed to retrieve the handler.')
            return None

        self._handler.run(*args, file_name=self._file_name)
        
        # The CSV task returns not the inserted items, but the name of the generated file
        # Note that it will be returned as many times as inputs received (e.g. rows inserted)
        
        return self._file_name