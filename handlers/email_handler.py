import smtplib

from typing import Dict, List

from config_manager import ConfigManager, ConfigType
from handlers.handler import Handler

class EmailHandler(Handler):
    
    
    def __init__(self):
        pass
    
    def run(self, *args: List, **kwargs: Dict) -> bool:
        config = ConfigManager.instance().get_config(ConfigType.SMTP)
        
        if config is None:
            print(__name__,'::run() could not retrieve SMTP configuration, ', kwargs)
            return kwargs
        
        file_name: str = kwargs.get('attachment_name')
        sender: str = kwargs.get('sender')
        recipient: List[str] = kwargs.get('recipient')
        subject: str = kwargs.get('subject')
        body: str = kwargs.get('body')

        
        smtp_server: str = config.get('server')
        smtp_user: str = config.get('user')
        smtp_pwd: str = config.get('password')
        
        if smtp_server is None:
            print(__name__,'::run() no SMTP server name provided, ', kwargs)
            return kwargs
                
        server: smtplib.SMTP = smtplib.SMTP(smtp_server)
        server.login(smtp_user, smtp_pwd)
        
        server.sendmail(sender, recepient, body)
        
        server.quit()
                
        return True