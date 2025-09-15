import os
import numpy as np
import pandas as pd
import datetime as dt
import time

def check_path():
    # check for save file path, create file if path not found
    # return dir_path, save_dir_path, planner_file_path, grader_file_path, planner_df, grader_df
    _dir_path = os.path.dirname(os.path.realpath(__file__))
    _save_dir_path = fr"{_dir_path:s}/Saves"
    _planner_file_path = fr"{_save_dir_path}/planner.csv"
    _grader_file_path = fr"{_save_dir_path}/grader.csv"
    if os.path.exists(_save_dir_path):
        if os.path.exists(_planner_file_path):
            _planner_df = pd.read_csv(_planner_file_path)
        else:
            _planner_df = pd.DataFrame()
        if os.path.exists(_grader_file_path):
            _grader_df = pd.read_csv(_grader_file_path)
        else:
            _grader_df = pd.DataFrame()
        print("pass")
    else:
        os.mkdir(_save_dir_path)
        _planner_df = pd.DataFrame()
        _grader_df = pd.DataFrame()
        print("make")
    
    return _dir_path, _save_dir_path, _planner_file_path, _grader_file_path, _planner_df, _grader_df

def check_assignment_date(_assignment_date):
    difference = _assignment_date-dt.datetime.now()
    hour_in_day = 24
    day, hour = divmod(difference.days*hour_in_day + difference.seconds/3600, 24)
    print(day, hour)
    hour, minute = divmod(hour*60, 60)
    print(hour, minute)

    return f"{day} day/days | {hour} hour/hours | {minute:.2f} minute/minutes"

if __name__ == "__main__":

    dir_path, save_dir_path, planner_file_path, grader_file_path, planner_df, grader_df = check_path()    

    test = dt.datetime.now() + dt.timedelta(days=5)
    print(test.day)
    time.sleep(5)
    print(check_assignment_date(test))



