# Classes for the project

import json
import os
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from ._version import VERSION


# Assignment model: represents a single assignment
class Assignment(BaseModel):
    name: str
    max_score: int
    deadline: Optional[str] = None  # string date '%d/%m/%y %H:%M:%S' eg. 28/09/25 13:55:26
    current_score: int = 0
    isDone: bool = False

    # Add version but don’t keep it in the model’s schema
    version: str = Field(default=VERSION, exclude=True)

    # Configure model to ignore unknown fields
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}


# Subject model: represents a course subject
class Subject(BaseModel):
    name: str
    credit: float
    assignments: List[Assignment] = []  # list of Assignment objects
    course_code: Optional[str] = None

    version: str = Field(default=VERSION, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}


# Semester model: represents a semester with multiple subjects
class Semester(BaseModel):
    year: Optional[str] = None
    season: Optional[str] = None
    subjects: List[Subject] = []

    version: str = Field(default=VERSION, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def to_dict(self):
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": VERSION}

    @classmethod
    def from_dict(cls, data: dict):
        # Pydantic can build the object directly from dict
        return cls(**data)


if __name__ == "__main__":
    # Save path for the semester.json file
    save_path = os.path.dirname(os.path.realpath(__file__))
    save_path = fr"{save_path:s}\..\Saves\semester.json"

    # Example assignments
    work1 = Assignment(name="work1", max_score=15)
    work2 = Assignment(name="work2", max_score=15)

    # Example subjects with assignments
    Cal = Subject(name="Cal 1", credit=3.0, assignments=[work1, work2])
    La = Subject(name="La", credit=3.0, assignments=[work1, work2])

    # Semester with subjects
    Fall_2025 = Semester(subjects=[Cal, La])

    # Save semester to JSON
    with open(save_path, "w") as f:
        json.dump(Fall_2025.to_dict(), f, indent=2)

    # Load semester back from JSON
    if os.path.exists(save_path):
        print("Save completed.")
        with open(save_path, "r") as f:
            data = json.load(f)
            loaded_semester = Semester.from_dict(data)

            # Print loaded data
            print(f"Semester: {loaded_semester}")
            for subject in loaded_semester.subjects:
                print(f"Subject: {subject}")
                for assignment in subject.assignments:
                    print(f"Assignment: {assignment}")
    else:
        print("Save failed")
