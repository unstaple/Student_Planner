# Classes for the project

import json
import os
from datetime import datetime as dt
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime as dt

try:
    from ._version import VERSION
except ImportError:
    from _version import VERSION

try:
    from .gradecal import calculate_gpa, get_grade_point
except ImportError:
    from gradecal import calculate_gpa, get_grade_point

try:
    from .utils import compare_time, format_timedelta
except ImportError:
    from utils import compare_time, format_timedelta

NUM_SPACES = 0

def spaces(n):
    return " "*n

# Assignment model: represents a single assignment
class Assignment(BaseModel):
    name: str
    max_score: float
    deadline: Optional[str] = None  # string date '%m/%d/%y %H:%M:%S' eg. 09/28/25 13:55:26
    status: str = None
    current_score: float = 0.0
    isDone: bool = False

    # Add version but don’t keep it in the model’s schema
    version: str = Field(default=VERSION, exclude=True)

    # Configure model to ignore unknown fields
    model_config = ConfigDict(extra="ignore")

    def update_deadline_status(self):
    
        if self.isDone:
            if not self.status == "Done":
                self.status = "Done"
            else:
                return None

        if self.deadline:
            diff_time = compare_time(dt.strptime(self.deadline, '%m/%d/%y %H:%M:%S'))
            _, info = format_timedelta(diff_time)
            totalMin = info[0]*60*24 + info[1]*60 + info[2]
            if 10080 > totalMin > 0: # info = [day, hour, minute]
                self.status = "Near Deadline"
            elif info[0] >= 10080:
                self.status = "Overdue"
            else:
                self.status = "Up Coming"
        else:
            self.status = "Not Done"

    def to_dict(self):
        self.update_deadline_status()
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}

    def show(self):
        self.update_deadline_status()
        return f"{spaces(NUM_SPACES + 4)}{self.name} | Score : {self.current_score}/{self.max_score}\n{spaces(NUM_SPACES + 4)}Status : {self.status} | Due : {self.deadline}\n"

# Subject model: represents a course subject
class Subject(BaseModel):
    name: str
    credit: float
    assignments: List[Assignment] = []  # list of Assignment objects
    course_code: Optional[str] = None
    if assignments:
        score: Optional[float] = sum(assignment.current_score for assignment in assignments if assignment.isDone)
    else:
        score: Optional[float] = 0.0

    grade: tuple = get_grade_point(score)

    version: str = Field(default=VERSION, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        self.update_score()
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}
    
    def info(self):
        self.update_score()
        return f"{spaces(NUM_SPACES + 2)}{self.course_code} {self.name} | Score : {self.score}/100 | Grade : {get_grade_point(self.score)[1]} | Credit : {self.credit}\n\n"
    
    def show(self) -> str:
        _outputString = self.info()
        if self.assignments:
            for assign in self.assignments:
                _outputString += assign.show() + "\n"
        else:
            _outputString += "No Current Assignment\n"

        return _outputString[:-1]

    def update_score(self) -> None:
        self.score = sum(assignment.current_score for assignment in self.assignments if assignment.isDone)

# Semester model: represents a semester with multiple subjects
class Semester(BaseModel):
    year: Optional[str] = None
    season: Optional[str] = None
    subjects: List[Subject] = []
    gpa: float = 0.0

    version: str = Field(default=VERSION, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        self.update_gpa()
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}

    def to_json(self):
        self.update_gpa()
        _save_path = os.path.dirname(os.path.realpath(__file__))
        _save_path = fr"{_save_path:s}\..\Saves"
        if self.year and self.season:
            name = f"{self.year}_{self.season}.json"
        else:
            i = 1
            while os.path.exists(f"{_save_path}\\Semester_{i}.json"):
                i += 1
            name = f"Semester_{i}.json"
        with open(f"{_save_path}\\{name}", "w") as f:
            json.dump(self.to_dict(), f, indent=2)

    def info(self) -> str:
        self.update_gpa()
        if self.year:
            _year = f" {self.year} "
        else:
            _year = ""
        if self.season:
            _season = f" {self.season} "
        else:
            _season = ""
        _outputString = f"{spaces(NUM_SPACES)}Semeter {_year}{_season}| GPA : {self.gpa}\n"
        
        return _outputString

    def show(self) -> str:
        _outputString = self.info()
        if self.subjects:
            for subject in self.subjects:
                _outputString += subject.show() + "\n\n"
        else:
            _outputString += f"\n\n{spaces(NUM_SPACES + 2)}No On Going Classes\n\n"

        return _outputString[:-1]

    def update_gpa(self) -> None:
        self.gpa = calculate_gpa(self)

    @classmethod
    def from_dict(cls, data: dict):
        # Pydantic can build the object directly from dict
        return cls(**data)

if __name__ == "__main__":
    # Save path for the semester.json file
    save_path = os.path.dirname(os.path.realpath(__file__))
    save_path = fr"{save_path:s}\..\Saves"

    # Example assignments
    work1 = Assignment(name="work1", max_score=15, deadline="10/03/25 13:55:26")
    work2 = Assignment(name="work2", max_score=15)

    # Example subjects with assignments
    Pscp = Subject(name="Pscp",course_code="06066303", credit=3.0, assignments=[work1, work2])
    work1.current_score = 65
    work1.isDone = True
    La = Subject(name="La", credit=3.0, assignments=[work1, work2])

    # Semester with subjects
    Fall_2025 = Semester(subjects=[Pscp, La], year="2025", season="Fall")
    Summer_2025 = Semester(subjects=[Pscp, La], year="2025", season="Summer")

    # Save semester to JSON
    Fall_2025.to_json()
    Summer_2025.to_json()

    # Load semester back from JSON
    names = [name for name in os.listdir(save_path)]
    for name in names:
        with open(f"{save_path}\\{name}", "r") as f:
            data = json.load(f)
            loaded_semester = Semester.from_dict(data)

            # Print loaded data
            print(loaded_semester.show())
