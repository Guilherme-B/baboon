import threading
import configparser as cp

from enum import Enum, unique
from typing import Dict, Union

@unique
class ConfigType(Enum):
    Reports = "reports"
    SMTP = "smtp"

class ConfigManager():

    __instance = None
    __singleton_lock = threading.Lock()
    
    __config: Dict[str, Dict[str, str]] = {}
    
    def __init__(self, auto_parse: bool = False):

        if ConfigManager.__instance != None:
            raise Exception(
                __name__, 
                '::__init__ an object of the class already exists.')
        else:
            ConfigManager.__instance = self
            
            self._parse_configs()
    
    @staticmethod
    def instance():

        if ConfigManager.__instance == None:
            with ConfigManager.__singleton_lock:
                if ConfigManager.__instance == None:
                    ConfigManager()

        return ConfigManager.__instance
    
    def _parse_configs(self) -> None:
        
        parser: cp.ConfigParser = cp.ConfigParser()
        
        parser.read("config/config.ini")
        
        for section in parser.sections():
            
            for config_type in ConfigType:
                if section == config_type.value:
                    self.__config[section] = dict(parser.items(section))
            
    def get_config(self, config_type: ConfigType, category: str = None) -> Union[None, Dict[str, str], str]:
        if category:
            return self.__config.get(config_type.value).get(category)
           
        return self.__config.get(config_type.value)