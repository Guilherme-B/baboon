
# Welcome to Baboon

Baboon aims at filling the gap between ETL libraries and manual reports.
By using Baboon, users can create ETL pipelines in a simple fashion as means of reducing manual labor when it comes to reporting. Even using Bonobo and other powerful libraries, one still has to create a script for each report and a wrapper around it. That's exactly what Baboon (original heh?) aims at solving.

# Pipeline Types

Baboon encompasses two possible pipeline types: automated and manual.

## Automated Pipelines

To run an automated pipeline, accessing the ReporManager's run() method will suffice.

    ReportManager(auto=True).instance().run()
    
This type of pipeline relies on the definition of a **report** and its **tasks** in a **JSON** file, which is automatically parsed, sorted and has its **DAG** built by Baboon. 

 For instance, the following **JSON** definition - which produces an Excel file with two tabs, one for each query and sends the file via email - would generate the subsequent **Bonobo DAG**:
 

    {
       "Marketing Department":[
          {
             "id":0,
             "name":"A Report",
             "frequency":"Weekly",
             "weekday":"Friday",
             "enabled":1,
             "tasks":[
                {
                   "id":1,
                   "name":"Customers Info",
                   "type":"query",
                   "statement":"select * from customer",
                   "server_name":"server_name",
                   "db_name":"db_name"
                },
                {
                   "id":2,
                   "name":"Sales Info",
                   "type":"query",
                   "statement":"select * from sales",
                   "server_name":"server_name",
                   "db_name":"db_name"
                },
                {
                   "id":3,
                   "name":"to_excel",
                   "type":"csv",
                   "file_name":"data.xlsx",
                   "parents":[
                      1,
                      2
                   ]
                },
                {
                   "id":4,
                   "name":"to_email",
                   "type":"email",
                   "unique":"True",
                   "recipient":"recipient@host.com",
                   "parents":[
                      3
                   ]
                }
             ]
          },
          (....)
    }

Generated DAG:
[![](https://mermaid.ink/img/eyJjb2RlIjoiZ3JhcGggTFJcbkFbUXVlcnkgVGFza10gLS0gVGFzayAxIC0tPiBCKChDU1YgVGFzaykpXG5FW1F1ZXJ5IFRhc2tdIC0tIFRhc2sgMiAgLS0-IEJcbkIgLS0gVGFzayAzIC0tPiBEW0VtYWlsIFRhc2tdIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)](https://mermaid-js.github.io/mermaid-live-editor/#/edit/eyJjb2RlIjoiZ3JhcGggTFJcbkFbUXVlcnkgVGFza10gLS0gVGFzayAxIC0tPiBCKChDU1YgVGFzaykpXG5FW1F1ZXJ5IFRhc2tdIC0tIFRhc2sgMiAgLS0-IEJcbkIgLS0gVGFzayAzIC0tPiBEW0VtYWlsIFRhc2tdIiwibWVybWFpZCI6eyJ0aGVtZSI6ImRlZmF1bHQifSwidXBkYXRlRWRpdG9yIjpmYWxzZX0)

## Manual Pipelines

Manual pipelines are accessible via the **ReportManager** singleton, which takes in children of the **Report** class which in turn, contains one or multiple instances of the **Task** class.

# Structure

## Report Manager

The report manager is a singleton agent which stores all the reports and drives the main logic, ensuring the right reports are ran at the right time.

## Report

The report class holds all the relevant characteristics of a report such as its name, run schedule, but most importantly, it contains the validation logic and the report's tasks.
## Task

Tasks drive the execution logic. They are runnables which translate to **Bonobo Nodes**, defining generic logic on which input to generate, and the corresponding output. For instance, a CSV Task would receive as input a series of rows, and output the name of the generated CSV file.
Tasks might contain handlers which drive I/O or networked operation.s

## Handler

Finally, handlers abstract the access logic, stowing away the I/O operations from the Task. In the example above, a CSV Writer Handler would create, open and write the input received by the CSV Task onto the actual CSV file.



# Upcoming Features & Requests

Baboon is a small library aimed at personal use. For this reason, features are developed on a personal need basis. However, requests are always welcome!

|                |Status|ETA|
|----------------|-------------------------------|-----------------------------|
|Report Scheduler|`Not Implemented`             |TBD|
|Automatic DAGs|`Not Implemented`            | Done          |


