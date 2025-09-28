import os
import datetime as dt
from google.oauth2.service_account import Credentials
from source import *
import json

def check_path() -> list:

    """
    Check for save file path, create file if path not found.
    
    Returns:
        _out (list):  [_dir_path (str) -> this directory path,
                                    _save_dir_path (str) -> Saves directory path,
                                    _semesters (list) -> list of semester objects]
    """

    _dir_path = os.path.dirname(os.path.realpath(__file__)) # this directory
    _save_dir_path = fr"{_dir_path:s}/Saves" # Saves directory
    
    _semesters = []

    for semeter_path in os.listdir(_save_dir_path):
        with open(_save_dir_path + "\\" + semeter_path, "r") as f:
            data = json.load(f)
            loaded_semester = Semester.from_dict(data)
            _semesters.append(loaded_semester)
    
    
    _out = [_dir_path, _save_dir_path, _semesters]
    
    return _out

def compare_time(_assignment_date : str) -> object:

    """
    Compare the time difference between assignment\'s dead line and current time.
    
    Args:
        _assigment_data (str): string that the represent time in "day/month/year hour:minute:second", "%m/%d/%y %H:%M:%S" format.
    
    Returns:
        _difference (object): timedelta between the deadline and current time.
    """

    _difference = _assignment_date-dt.datetime.now() # Deadline - current time.

    return _difference

def format_timedelta(_time : object):

    """
    Format timedelta to readable string.

    Args:
        _time (object): timedelta object

    Returns:
        _formatted_str (str): readable string of that timedelta.
    """

    hour_in_day = 24
    # get day and hour by getting timedelta's days times 24 plus timedelta's seconds divided by 3600 to get total hours
    # then divided by 24 to get days and the remaining as hours.
    day, hour = divmod(_time.days*hour_in_day + _time.seconds/3600, 24)
    #  get hour and minute by hour times 60 and then devided again to get modded hours and the remaining as minutes.
    hour, minute = divmod(hour*60, 60)
    _formatted_str = f"{day} day/days | {hour} hour/hours | {minute:.2f} minute/minutes"

    return _formatted_str

if __name__ == "__main__":

    dir_path, save_dir_path, semesters = check_path()
    print(semesters)

    test = dt.datetime.now() + dt.timedelta(days=5)
    diff_time = compare_time(test)
    print(format_timedelta(diff_time))
