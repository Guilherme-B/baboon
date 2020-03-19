from tasks.task import Task
from handlers.email_handler import EmailHandler

class TaskEmail(Task):
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
         # Should a single email be sent regardless of the number of node returned arguments
        self._unique: bool  = kwargs.get('unique', True)
        self._attachment_dir: str = kwargs.get('attachment')
        
        self._handler = EmailHandler()
        
    def validate(self):
        pass
        
    def run(self, *args, **kwargs):

        if self._unique and self._run_count > 1 :
            return None
            
        return self._handler.run(*args, attachment_name=self._attachment_dir)