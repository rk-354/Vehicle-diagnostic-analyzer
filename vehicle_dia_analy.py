import argparse
import datetime
import os
import pandas
import typing  # local import src.plotter

def generate_vehicle_diagnostic_plots_from_data(input_directory: str, output_directory: str, should_rename: bool):
    input_files: typing.List[str] = os.listdir(input_directory)
    
    if input_files is None:
        print(f"No files found in directory: {input_directory}")
        return 1
    
    print(f"{len(input_files)} files found.")
    
    dataframes = []
    for log_filename in input_files:
        full_log_file_path = os.path.join(input_directory, log_filename)
        
        # First 2 rows in Vehicle Diagnostic data files are the heading and the date.
        dataframes.append(pandas.read_csv(full_log_file_path, skiprows=2))
        
        if should_rename:
            rename_log_file_using_date(full_log_file_path)

    src.plotter.create_aggregated_plot(dataframes, output_directory)

def rename_log_file_using_date(log_full_path: str, new_log_filename_suffix="__VehicleDiagnosticLog.csv"):
    """
    By default, Vehicle Diagnostic log files are just saved with the name 'My Vehicle Diagnostic Data Logs',
    which is not very helpful.
    
    Given a Vehicle Diagnostic log file name, this function renames it to be:
    <Date>_VehicleDiagnosticLog.csv
    where the Date is pulled from the header of the file itself.
    """
    
    # example: "Jul 23, 2018 8:18:31 AM"
    diagnostic_timestamp_format = "%b %d, %Y %I:%M:%S %p"
    # The format of the timestamp used in the filename
    
    # example: 20180723-081831
    desired_timestamp_format = "%Y%m%d-%H%M%S"
    
    # Can't rename file while its open
    log_file_timestamp = ""
    
    with open(log_full_path, 'r') as log_file_handle:
        file_timestamp = log_file_handle.readlines()[1].strip()
        log_file_timestamp = datetime.datetime.strptime(
            file_timestamp, diagnostic_timestamp_format).strftime(desired_timestamp_format)
    
    log_file_folder = os.path.split(log_full_path)[0]
    new_log_file_full_path = os.path.join(
        log_file_folder, log_file_timestamp + new_log_filename_suffix)
    
    os.rename(log_full_path, new_log_file_full_path)
    print(f"[DEBUG] Renamed {os.path.basename(log_full_path)} to {new_log_file_full_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-folder", 
                        help="Input directory: where Vehicle Diagnostic data files are stored", 
                        type=str, required=True)
    parser.add_argument("-o", "--output-folder", 
                        help="Output directory: where output graphs will be stored", 
                        type=str, required=True)
    parser.add_argument("-r", "--rename", action="store_true", 
                        help="Whether or not you'd like the files to be renamed", required=True)
    
    args = parser.parse_args()
    
    generate_vehicle_diagnostic_plots_from_data(
        args.input_folder, args.output_folder, args.rename)
