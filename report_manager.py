import threading

from json import loads
from os import path
from collections import defaultdict
from typing import AnyStr, DefaultDict, Dict, List

from config_manager import ConfigManager
from report import Report

import bonobo


class ReportManager():
    """[The ReportManager singleton class is responsible for holding and driving the main Report pipeline.]

    Raises:
        Exception: Singleton object already created.

    Returns:
        None
    """

    __instance = None
    __singleton_lock = threading.Lock()
    __config: Dict[str, Ditct[str, str]] = {}
    
    _reports: DefaultDict[str, list] = defaultdict(list)

    def __init__(self, auto_parse: bool = False):

        if ReportManager.__instance != None:
            raise Exception(
                __name__, 
                '::__init__ an object of the class already exists.')
        else:
            ReportManager.__instance = self

        # Initialize the config manager
        ConfigManager.instance()
        
        # If auto parsing is enabled, parse the reports according to the .JSON source
        if auto_parse:
            self._parse_reports()

    @staticmethod
    def instance():

        if ReportManager.__instance == None:
            with ReportManager.__singleton_lock:
                if ReportManager.__instance == None:
                    ReportManager()

        return ReportManager.__instance

    def reports(self) -> DefaultDict[str, List]:
        return self._reports

    def append(self, department_name: str, report_item: Report) -> None:
        if department_name is None:
            print(__name__, 
                  '::append(...) invalid department_name, ',
                  department_name)
            return

        if report_item is None:
            print(__name__, 
                  '::append(...) invalid report_item, ', 
                  report_item)
            return
        
        self._reports[department_name].append(report_item)

    def _valid(self, rep: Report) -> bool:
        # ToDo - Validate if the report is on the proper schedule day.

        return True

    
    def _parse_reports(self) -> None:
        reports_full_path: str = './config/reports.json'

        if path.exists(reports_full_path):

            with open(reports_full_path, 'r') as reports_source:
                file: AnyStr = reports_source.read()

                if file is not None:
                    data = loads(file)

                    if data is not None:
                        for department in data:
                            for report_data in data[department]:
                                
                                report_instance: Report = Report(report_data)
        
                                if report_instance is not None:
                                    self.append(department, report_instance)
        else:
            print(__name__, 
                  "::parse_reports() invalid reports source.")
            return

    def run(self) -> bool:
        # TODO: Change the continue to a report error insertion on DB

        if self._reports is None:
            print(__name__, 
                  "::run() no reports available.")
            return False

        for dep_report in self._reports.values():
            if dep_report is not None:
                for report in dep_report:

                    if not report.enabled:
                        print(__name__, '::run() report is disabled, ',
                              report.name)
                        continue

                    graph: Bonobo.graph = report.generate_graph()

                    if graph is None:
                        print(__name__,
                              "::run() DAG could not be constructed, ", 
                              report.name)
                        continue

                    if self._valid(report):
                        print(__name__,
                              ' Running report '
                              , report.name)
                        
                        bonobo.run(graph)
