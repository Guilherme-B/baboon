import pyodbc

from typing import Any, List

from handlers.handler import Handler

class QueryHandler(Handler):
    
    def __init__(self):
       super()

    def run(self, *args, **kwargs) -> List[Any]:        
        server_name = kwargs.get('server_name')
        db_name = kwargs.get('db_name')
        statement = kwargs.get('statement')
        
        if statement is None:
            print(__name,"::run() invalid statement provided,", statement)
            return
        
        if server_name is None or db_name is None:
            print(__name__,"::run() invalid arguments supplied for connection,", kwargs)
            return
                
        conn = None
        
        try:
            conn = pyodbc.connect(
                f"Driver=""{SQL Server Native Client 11.0}"";"
                f"Server={server_name};"
                f"Database={db_name};"
                f"Trusted_Connection=yes;", timeout = 5)
        
            if conn is not None:
                cursor = conn.cursor()
                cursor.execute(statement)
                
                for row in cursor:
                    yield row
            
        except pyodbc.DatabaseError as e:
            print(__name__, '::run() could not connect to the server, ', e)
        except pyodbc.Error as e:
            print(__name__, '::run() could not run the specified query, ', e)
        finally:
            if conn is not None:
                conn.close()
