import os
import numpy as np
import pandas as pd
import datetime as dt
import time

def check_path() -> list:
    '''
    Check for save file path, create file if path not found.

    return list of strings v
    _dir_path (str) -> this directory path.
    _save_dir_path (str) -> Saves directory path.
    _planner_file_path (str) -> planner.csv path.
    _grader_file_path (str) -> grader.csv path.
    _planner_df (str) -> planner DataFrame.
    _grader_df (str) -> grader DataFrame.
    '''
    _dir_path = os.path.dirname(os.path.realpath(__file__)) # this directory
    _save_dir_path = fr"{_dir_path:s}/Saves" # Saves directory
    _planner_file_path = fr"{_save_dir_path}/planner.csv" # planner.csv path
    _grader_file_path = fr"{_save_dir_path}/grader.csv" # grader.csv path
    if os.path.exists(_save_dir_path): # if Saves directory exist.
        if os.path.exists(_planner_file_path): # if planner.csv exist, read the csv.
            _planner_df = pd.read_csv(_planner_file_path)
        else: # else create the planner DataFrame then create an empty csv file.
            _planner_df = pd.DataFrame()
            _planner_df.to_csv(_planner_file_path)
        if os.path.exists(_grader_file_path): # if grader.csv exist, read the csv.
            _grader_df = pd.read_csv(_grader_file_path)
        else: # else create the grader DataFrame then create an empty csv file.
            _grader_df = pd.DataFrame()
            _grader_df.to_csv(_grader_file_path)
    else: # if Saves directory doesn't exist or else, create planner & grader DataFrame and then create an empty csv.
        os.mkdir(_save_dir_path)
        _planner_df = pd.DataFrame()
        _grader_df = pd.DataFrame()
        _planner_df.to_csv(_planner_file_path)
        _grader_df.to_csv(_grader_file_path)

    return [_dir_path, _save_dir_path, _planner_file_path, _grader_file_path, _planner_df, _grader_df]

def compare_time(_assignment_date : str) -> object:
    '''
    Compare the time difference between assignment\'s dead line and current time.

    arg v
    _assigment_data (str) -> string that the represent time in "day/month/year hour:minute:second", "%m/%d/%y %H:%M:%S" format.
    return value v
    _difference (object) -> timedelta between the deadline and current time.
    '''
    _difference = _assignment_date-dt.datetime.now() # Deadline - current time.

    return _difference

def format_timedelta(_time : object):
    '''
    Format timedelta to readable string.

    arg v
    _time (object) -> timedelta object
    return v
    _formatted_str (str) -> readable string of that timedelta.
    '''
    hour_in_day = 24
    # get day and hour by getting timedelta's days times 24 plus timedelta's seconds divided by 3600 to get total hours
    # then divided by 24 to get days and the remaining as hours.
    day, hour = divmod(_time.days*hour_in_day + _time.seconds/3600, 24)
    #  get hour and minute by hour times 60 and then devided again to get modded hours and the remaining as minutes.
    hour, minute = divmod(hour*60, 60)
    _formatted_str = f"{day} day/days | {hour} hour/hours | {minute:.2f} minute/minutes"

    return _formatted_str

if __name__ == "__main__":

    dir_path, save_dir_path, planner_file_path, grader_file_path, planner_df, grader_df = check_path()

    test = dt.datetime.now() + dt.timedelta(days=5)
    diff_time = compare_time(test)
    print(format_timedelta(diff_time))
