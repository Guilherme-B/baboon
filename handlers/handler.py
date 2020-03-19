from abc import ABC, abstractmethod
from enum import Enum, unique

import bonobo

class HandlerType(Enum):
    CSV = "CSV",
    QUERY = "QUERY",

class Handler(ABC):
    
    def __init__(self):
        pass
    
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError