from handlers.query_handler import QueryHandler
from tasks.task import Task

class TaskQuery(Task):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self._server: str = kwargs.get('server_name')
        self._database: str = kwargs.get('db_name')
        self._statement: str = kwargs.get('statement')
        
        self._handler = QueryHandler()
        
    def validate(self):
        return  self._server is not None and \
                self._database is not None and \
                self._statement is not None
    
    def run(self, *args, **kwargs):
                
        if self._handler is not None:

            return self._handler.run(**{
                    'server_name': self._server,
                    'db_name': self._database,
                    'statement': self._statement,
                })