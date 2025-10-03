# Classes for the project

import json
from datetime import datetime as dt
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict

try:
    from ._version import version
    from .gradecal import calculate_gpa, get_grade_point
    from .utils import compare_time, saves_dir
except Exception:
    from gradecal import calculate_gpa, get_grade_point
    from utils import compare_time, saves_dir
    try:
        from _version import version
    except Exception:
        version = "0.0.0"

NUM_SPACES = 0

def spaces(n: int) -> str:
    return " " * n

class Assignment(BaseModel):
    name: str
    max_score: float
    deadline: Optional[str] = None  # '%m/%d/%y %H:%M:%S'
    current_score: float = 0.0
    isDone: bool = False
    status: Optional[str] = None

    version: str = Field(default=version, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def update_deadline_status(self) -> None:
        """Set status field based on done flag and deadline relative to now."""
        if self.isDone:
            self.status = "Done"
            return

        if not self.deadline:
            self.status = "Not Done"
            return

        try:
            deadline_dt = dt.strptime(self.deadline, "%m/%d/%y %H:%M:%S")
        except Exception:
            self.status = "Invalid Deadline"
            return

        diff = compare_time(deadline_dt)
        total_minutes = diff.total_seconds() / 60.0

        if total_minutes < 0:
            self.status = "Overdue"
        elif total_minutes <= 7 * 24 * 60:  # within one week
            self.status = "Near Deadline"
        else:
            self.status = "Up Coming"

    def to_dict(self) -> dict:
        self.update_deadline_status()
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": version}

    def show(self) -> str:
        self.update_deadline_status()
        return f"{spaces(NUM_SPACES + 4)}{self.name} | Score : {self.current_score}/{self.max_score}\n{spaces(NUM_SPACES + 4)}Status : {self.status} | Due : {self.deadline}\n"

class Subject(BaseModel):
    name: str
    credit: float
    assignments: List[Assignment] = Field(default_factory=list)
    course_code: Optional[str] = None

    version: str = Field(default=version, exclude=True)
    model_config = ConfigDict(extra="ignore")

    @property
    def score(self) -> float:
        """Compute score as sum of current_score for assignments marked done."""
        return sum(a.current_score for a in self.assignments if a.isDone)

    @property
    def grade(self):
        return get_grade_point(self.score)

    def to_dict(self) -> dict:
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": version}

    def info(self) -> str:
        gp = get_grade_point(self.score)
        return f"{spaces(NUM_SPACES + 2)}{self.course_code or ''} {self.name} | Score : {self.score}/100 | Grade : {gp[1]} | Credit : {self.credit}\n\n"

    def show(self) -> str:
        out = self.info()
        if self.assignments:
            for a in self.assignments:
                out += a.show() + "\n"
        else:
            out += f"{spaces(NUM_SPACES + 4)}No Current Assignment\n"
        return out.rstrip("\n")

class Semester(BaseModel):
    year: Optional[str] = None
    season: Optional[str] = None
    subjects: List[Subject] = Field(default_factory=list)
    gpa: float = 0.0
    file_path: str = None

    version: str = Field(default=version, exclude=True)
    model_config = ConfigDict(extra="ignore")

    def to_dict(self) -> dict:
        self.update_gpa()
        return self.model_dump(exclude={"version"}, exclude_none=True) | {"version": version}

    def to_json(self) -> None:
        """Save semester to Saves directory with a sensible filename."""
        self.update_gpa()
        save_path = saves_dir()
        if self.year and self.season:
            self.file_path = f"{self.year}_{self.season}.json"
        else:
            i = 1
            while (save_path / f"Semester_{i}.json").exists():
                i += 1
            self.file_path = f"Semester_{i}.json"
        with (save_path / self.file_path).open("w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=2)
        
    def delete(self) -> None:
        save_path = saves_dir()
        target = save_path / self.file_path if self.file_path else None
        if target and target.exists():
            target.unlink()

    def info(self) -> str:
        self.update_gpa()
        y = f" {self.year} " if self.year else ""
        s = f" {self.season} " if self.season else ""
        return f"{spaces(NUM_SPACES)}Semester{y}{s}| GPA : {self.gpa}\n"

    def show(self) -> str:
        out = self.info()
        if self.subjects:
            for subject in self.subjects:
                out += subject.show() + "\n\n"
        else:
            out += f"\n\n{spaces(NUM_SPACES + 2)}No On Going Classes\n\n"
        return out.rstrip("\n")

    def update_gpa(self) -> None:
        self.gpa = calculate_gpa(self)
    

    @classmethod
    def from_dict(cls, data: dict):
        # pydantic will convert nested dicts to models when possible
        return cls(**data)

if __name__ == "__main__":
    # Save path for the semester.json file
    save_path = saves_dir()

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
    for p in sorted(save_path.iterdir()):
        if p.suffix == ".json":
            with p.open("r", encoding="utf-8") as f:
                data = json.load(f)
            loaded_semester = Semester.from_dict(data)
            print(loaded_semester.show())
