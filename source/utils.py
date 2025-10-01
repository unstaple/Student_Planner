# Utilities functions

import json
import os
from datetime import datetime as dt, timedelta
import time

def clear() -> None:
    if os.name == 'nt':       # Windows
        os.system('cls')
    else:                     # macOS / Linux / other POSIX
        os.system('clear')

def check_path() -> list[object]:

    """
    Check for all semesters inside the Saves folder
    
    Returns:
        _semesters (list) -> list of semester objects
    """

    try:
        from classes import Semester
    except ImportError:
        from .classes import Semester

    _dir_path = os.path.dirname(os.path.realpath(__file__)) # this directory
    _save_dir_path = f"{_dir_path:s}\\..\\Saves" # Saves directory

    _semesters = []

    for semeter_path in os.listdir(_save_dir_path):
        with open(_save_dir_path + "\\" + semeter_path, "r") as f:
            data = json.load(f)
            loaded_semester = Semester.from_dict(data)
            _semesters.append(loaded_semester)

    return _semesters

def compare_time(_assignment_date : timedelta) -> object:

    """
    Compare the time difference between assignment\'s dead line and current time.
    
    Args:
        _assigment_data (str): string that the represent time in "day/month/year hour:minute:second", "%m/%d/%y %H:%M:%S" format.
    
    Returns:
        _difference (object): timedelta between the deadline and current time.
    """

    _difference = _assignment_date-dt.now() # Deadline - current time.

    return _difference

def format_timedelta(_time : object) -> tuple[str, list]:

    """
    Format timedelta to readable string.

    Args:
        _time (datetime.timedelta): timedelta object

    Returns:
        formatted string, info list [days, hours, minutes]
    """

    hour_in_day = 24
    # get day and hour by getting timedelta's days times 24 plus timedelta's seconds divided by 3600 to get total hours
    # then divided by 24 to get days and the remaining as hours.
    total_hours = _time.days * hour_in_day + _time.seconds / 3600.0
    day, hour = divmod(total_hours, 24)
    # get hour and minute
    hour, minute = divmod(hour * 60, 60)
    _formatted_str = f"{int(day)} day/days | {int(hour)} hour/hours | {int(minute)} minute/minutes"
    _info = [int(day), int(hour), int(minute)]

    return (_formatted_str, _info)

def deadline_report(semesters : list[object]) -> None:
    """
    Format deadline notice into a readable string

    Returns:
        deadlineReport (str): Formatted string deadline notice
    """
    textlist = []
    for semester in semesters:
        for subject in semester.subjects:
            for assignment in subject.assignments:
                if assignment.status == "Near Deadline":
                    _, info = format_timedelta(compare_time(dt.strptime(assignment.deadline, '%m/%d/%y %H:%M:%S')))
                    textlist.append(f"  --> Semester : {semester.season} {semester.year} | Class : {subject.name} | Name : {assignment.name}\n Remaing Time  --> Day : {info[0]} | Hour : {info[1]} | Minute : {info[2]}\n")
    
    if textlist:
        print("\nAssignments that are near the deadline\n")
        for text in textlist:
            print(text)


if __name__ == "__main__":

    now = dt.now()
    time.sleep(5)
    test = now + timedelta(days=5)
    diff_time = compare_time(test)
    print(format_timedelta(diff_time))
