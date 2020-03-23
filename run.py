import argparse
import configparser

from report_manager import ReportManager
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Basic temporary ETL pipeline until Airflow is available.")
    
    parser.add_argument('-r', '--reports', help='Select individual reports based on their ID, separated by a space.', type= str, nargs='+', required=False)
    parser.add_argument('-v', '--visualize', help="Generate the GraphViz visuals for each report and its tasks. Note: this option is mutually exclusive, prevents the reports from being ran.", type=int, nargs='?', required=False, default= 0)
    
    args = parser.parse_args()

    ReportManager(True).instance().run()