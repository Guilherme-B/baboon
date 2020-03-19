from dataclasses import dataclass
from enum import auto, Enum, unique
from typing import Any, ClassVar, Dict, List, Union

from handlers.handler import Handler, HandlerType
from handlers.csv_handler import CSVHandler
from handlers.query_handler import QueryHandler

from tasks.task import Task
from tasks import *

import bonobo

@unique
class ReportFrequency(Enum):
    DAILY = "daily",
    WEEKLY = "weekly",
    MONTHLY = "monthly",
    QUARTERLY = "quarterly",
    YEARLY = "yearly",
    OTHERS = "others"
    
@unique
class WeekDay(Enum):
    MONDAY = auto(),
    TUESDAY = auto(),
    WEDNESDAY = auto(),
    THURSDAY = auto(),
    FRIDAY = auto(),
    SATURDAY = auto(),
    SUNDAY = auto()
    
@dataclass
class Query:
    name: str
    order: int
    statement: str

class Report():
        
    def __init__(self, json_str: str):
        
        if json_str is None:
            print(__name__, '::__init__ invalid input, ', json_str)
            return 

        self._id: int = json_str.get("id", -1)
        self._name: str = json_str.get("name", None)
        self._enabled: bool = json_str.get("enabled", False)
        
        self._frequency: ReportFrequency = None
        self._frequency_day: Union[None, WeekDay] = None
        
        self._tasks: Dict[Dict, Task] = dict()

        try:
            freq: str = json_str.get("frequency", None)
            self._frequency = ReportFrequency[freq.upper()]
        except (AttributeError, KeyError) as e:
            print(__class__.__name__, '::__init__ invalid frequency input, ', freq, ' ,', e)
            return
    
        try:
            weekday: str = json_str.get("weekday", None)
            self._frequency_day = WeekDay[weekday.upper()]
        except (AttributeError, KeyError) as e:
            print(__name__, '::__init__ invalid weekly input, ', weekday, ' ,', e)
            return 

        self._generate_tasks(json_str)
        
        if not self._validate(True):
            return
          
    def _generate_tasks(self, data_json: str) -> None:
        """[summary]
        
        Two steps:
            1- Create each task based on the .JSON definition
            2- Assess each task's children
        
        Arguments:
            data_json {str} -- [JSON file containing the report's Tasks' definition.]
        
        Returns:
            None
        """

        # Create a task as defined on the report's JSON children.
        for tsk in data_json.get('tasks', dict()):
            if tsk is not None:
                
                # Fetch the task's type and initialize the corresponding Task%name% Class should it exist
                try:
                    tsk_class: str = tsk.get("type").title()
                    task_class_type: Task = globals()[f"Task{tsk_class}"]
                    task_id: int = tsk.get("id")

                    self._tasks[task_id] = task_class_type(**tsk)
                except (AttributeError, KeyError) as e:
                    print(__name__, '::__init__ invalid task type input for task,', e)
                    continue 
                
        # Build the dependencies graph, that is, update the parents and children for each node (Task)
        tasks: Dict[int, Task] = self._tasks

        for tsk in tasks.values():
            # Find the node's parents, and update the parent's child listing with the current node's ID
            parents: List[int] = tsk.parents

            if parents is not None:
                #print(tsk.id, ":", len(parents))
                for parent_id in parents:
                    tasks[parent_id].add_child(tsk.id)
                    #print("Adding child:", tsk.id, "; to parent:", parent_id)
        

    def _validate(self, verbose:bool = False) -> bool:

        if self._id < 0:
            raise ValueError(__name__, "::_validate() invalid Report id,", self._id)
            return False
        
        if self._tasks is not None:
            for tsk in self._tasks.values():
                if tsk is not None:
                    if not tsk.validate():
                        return False
        else:
            print(__name__, '::_validate() tasks not found.')
            return False
              
        if self._frequency == ReportFrequency.WEEKLY and self._frequency_day is None:
            print(__name__, '::_validate() invalid using weekly frequency requires the use of day indication.')
            return False
              
        return True
    
    def generate_graph(self) -> Union[bonobo.Graph, None]:
        """[Generate the Bonobo.Graph for the current Report]
        
            The report generation follows the rules:
            - Tasks which do not depend on any are executed in parallel
            - Tasks which depend on a given task await the previous' completion to be executed
            
        Returns:
            bonobo.Graph -- [The generated bonobo.Graph]
        """
        graph: bonobo.Graph = bonobo.Graph()
                
        #Generate a dependencies 1-d tree, (child_id, parent_id) so we can isolate parents
        # Parent: graph.add_chain(parent, _input= None)
        # Child : graph.add_chain(child1, _output = parent)
        tasks: Dict[int, Task] = self._tasks
        
        # Start by adding all the Tasks as Orhphan nodes
        for tsk in tasks.values():
            graph.add_node(tsk)

        # Assess the nodes' relationships and connect them as input or output (or both)
        for node in tasks.values():
            if node.children is not None:
                for child_id in node.children:
                    if child_id is not None:
                        # For some reason _input isn't working as expected, remove it
                        graph.add_chain(_input = tasks[child_id], _output= node)   
                        #graph.add_chain(tasks[child_id], _output= node)     
            else:
                graph.add_chain(node, _input=None)          
                        
        '''for task in sorted_tasks.values():

            graph.add_chain(
                *((task(),) if task else ()),
                #_input = sorted_tasks[task.depends_on] if task.depends_on else ()
            )'''
        
        # Old method: single straight graph
        #sorted_tasks: Dict[int, Task] = {k: v for k,v in sorted(self._tasks.items(), key = lambda item: item[0])}
        #graph.add_chain(*sorted_tasks.values())

        return graph if len(graph.nodes) > 0 else None
    
        
    @property
    def enabled(self) -> bool:
        return self._enabled    
    
    @property
    def name(self) -> str:
        return self._name