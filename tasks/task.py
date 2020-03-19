from abc import ABC, abstractmethod
from typing import List, Union

from handlers.handler import Handler

import bonobo

class Task():
    
    __metaclass__ = ABC
    
    def __init__(self, *args, **kwargs):
        
        self._id: int = kwargs.get('id')
        self._name: str = kwargs.get('name')
        
        self._handler: Handler = None
        self._parents: List[int] = kwargs.get('parents')
        
        # Stores the amount of times the Task instance has ran.
        # Useful for limiting to single-shot use (for instance, e-mail sending)
        self._run_count: int = 0
        self._children: List[int] = None
    
    @abstractmethod
    def validate(self):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        self._run_count += 1
        return self.run(*args, **kwargs)
    
    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def parents(self) -> Union[List[int], None]:
        return self._parents
    
    @property 
    def id(self) -> id:
        return self._id 
    
    @property
    def children(self) -> Union[List[int], None]:
        return self._children
    
    def add_child(self, child_id: int) -> None:
        if child_id is None:
            return
            
        if not self._children:
            self._children = []
            
        self._children.append(child_id)
