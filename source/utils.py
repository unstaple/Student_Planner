import json
import os
from pathlib import Path
from datetime import datetime as dt, timedelta
from typing import List

def clear() -> None:
    """Clear the terminal in a cross-platform way."""
    os.system('cls' if os.name == 'nt' else 'clear')

def saves_dir() -> Path:
    """Return Path to Saves directory, creating it if necessary."""
    dir = Path(__file__).resolve().parent.parent / "Saves"
    dir.mkdir(parents=True, exist_ok=True)
    return dir

def check_path() -> List[object]:
    """
    Load all semester JSON files from Saves directory and return list of Semester objects.
    """
    try:
        from classes import Semester
    except ImportError:
        from .classes import Semester

    out: List[Semester] = []
    for p in saves_dir().glob("*.json"):
        try:
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            loaded = Semester.from_dict(data)
            out.append(loaded)
        except Exception:
            # don't crash on a bad file; skip it
            continue
    return out

def compare_time(assignment_datetime: dt) -> timedelta:
    """
    Return timedelta between the given assignment datetime and now: (deadline - now).
    """
    return assignment_datetime - dt.now()

def format_timedelta(td: timedelta) -> tuple[str, List[int]]:
    """
    Convert a timedelta into a human-readable string and a [days, hours, minutes] list.

    Always uses absolute values for readability; callers should check sign of original timedelta
    to decide if it's overdue or upcoming.
    """
    total_seconds = int(abs(td.total_seconds()))
    days, rem = divmod(total_seconds, 86400)  # seconds in a day
    hours, rem = divmod(rem, 3600)
    minutes, _ = divmod(rem, 60)

    s = f"{days} day/days | {hours} hour/hours | {minutes} minute/minutes"
    return s, [int(days), int(hours), int(minutes)]

def deadline_report(semesters: List[object]) -> None:
    """
    Format deadline notice into a readable string

    Returns:
        deadlineReport (str): Formatted string deadline notice
    """
    from datetime import datetime as dt

    if not semesters:
        print("No semesters loaded.")
        return

    notices = []
    for semester in semesters:
        for subject in semester.subjects:
            for assignment in subject.assignments:
                if not assignment.deadline:
                    continue
                try:
                    deadline_dt = dt.strptime(assignment.deadline, "%m/%d/%y %H:%M:%S")
                except Exception:
                    continue
                diff = compare_time(deadline_dt)
                # near deadline = between 0 and 7 days remaining
                if 0 < diff.total_seconds() <= 7 * 24 * 3600:
                    _, info = format_timedelta(diff)
                    notices.append(
                        f"  --> Semester : {semester.season} {semester.year} | Class : {subject.name} | "
                        f"Name : {assignment.name}\n    Remaining -> Day: {info[0]} | Hour: {info[1]} | Minute: {info[2]}\n"
                    )

    if notices:
        print("\nAssignments that are near the deadline\n")
        for n in notices:
            print(n)
    else:
        print("\nNo assignments are near deadline.\n")
