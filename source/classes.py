# Classes for the project

import json
import os
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
try:
    from ._version import VERSION
except ImportError:
    from _version import VERSION
try:
    from .gradecal import *
except ImportError:
    from gradecal import *


# Assignment model: represents a single assignment
class Assignment(BaseModel):
    name: str
    max_score: float
    deadline: Optional[str] = None  # string date '%d/%m/%y %H:%M:%S' eg. 28/09/25 13:55:26
    current_score: float = 0.0
    isDone: bool = False

    # Add version but don’t keep it in the model’s schema
    version: str = Field(default=VERSION, exclude=True)

    # Configure model to ignore unknown fields
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}

    def show(self):
        return f"     {self.name} | {self.current_score}/{self.max_score} | {self.deadline} | {self.isDone}"


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
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}
    
    def show(self) -> str:
        _outputString = f"   {self.course_code} | {self.name} | Score : {self.score}/100 | Credit : {self.credit}\n"
        for assign in self.assignments:
            _outputString += assign.show() + "\n"

        return _outputString[:-1]

# Semester model: represents a semester with multiple subjects
class Semester(BaseModel):
    year: Optional[str] = None
    season: Optional[str] = None
    subjects: List[Subject] = []
    course_data: List[tuple[float]] = [(subj.score, subj.credit) for subj in subjects] if subjects else []
    gpa: float = calculate_gpa(course_data)

    version: str = Field(default=VERSION, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}

    def to_json(self):
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
        if self.year:
            _year = f" {self.year} "
        else:
            _year = ""
        if self.season:
            _season = f" {self.season} "
        else:
            _season = ""
        _outputString = f"Semeter {_year}{_season}| GPA : {self.gpa}\n"
        
        return _outputString

    def show(self) -> str:
        _outputString = self.info()
        for subject in self.subjects:
            _outputString += subject.show() + "\n\n"

        return _outputString[:-1]

    @classmethod
    def from_dict(cls, data: dict):
        # Pydantic can build the object directly from dict
        return cls(**data)


if __name__ == "__main__":
    # Save path for the semester.json file
    save_path = os.path.dirname(os.path.realpath(__file__))
    save_path = fr"{save_path:s}\..\Saves"

    # Example assignments
    work1 = Assignment(name="work1", max_score=15)
    work2 = Assignment(name="work2", max_score=15)

    # Example subjects with assignments
    Pscp = Subject(name="Pscp",course_code="06066303", credit=3.0, assignments=[work1, work2])
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
