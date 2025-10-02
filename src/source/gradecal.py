# Grade calculation functions

from typing import Tuple

def get_default_thresholds():
    """
    Return default grade thresholds in descending order.
    """
    return {
        'A': 80,
        'B+': 75,
        'B': 70,
        'C+': 65,
        'C': 60,
        'D+': 55,
        'D': 50,
        'F': 0
    }

def get_grade_point(score: float) -> Tuple[float, str]:
    """
    Convert raw score to (grade_point, letter_grade).
    If score is None or not a number, treat as 0 (F).
    """
    try:
        s = float(score)
    except Exception:
        s = 0.0

    thresholds = get_default_thresholds()
    grade_points = {
        'A': 4.0,
        'B+': 3.5,
        'B': 3.0,
        'C+': 2.5,
        'C': 2.0,
        'D+': 1.5,
        'D': 1.0,
        'F': 0.0
    }

    # iterate thresholds in descending order by min_score
    for grade, min_score in sorted(thresholds.items(), key=lambda x: x[1], reverse=True):
        if s >= min_score:
            return grade_points[grade], grade
    return 0.0, 'F'

def calculate_gpa(semester) -> float:
    """
    Calculate GPA for a semester object.
    """
    total_grade_points = 0.0
    total_credits = 0.0

    for subject in semester.subjects:
        gp, _ = get_grade_point(subject.score)
        total_grade_points += gp * (subject.credit or 0.0)
        total_credits += (subject.credit or 0.0)

    if total_credits == 0:
        return 0.0
    return total_grade_points / total_credits

def calculate_gpax(all_semesters: list) -> float:
    """
    Calculate GPAX across a list of semesters.
    """
    total_grade_points = 0.0
    total_credits = 0.0
    for sem in all_semesters:
        for subject in sem.subjects:
            gp, _ = get_grade_point(subject.score)
            total_grade_points += gp * (subject.credit or 0.0)
            total_credits += (subject.credit or 0.0)
    if total_credits == 0:
        return 0.0
    return total_grade_points / total_credits

if __name__ == "__main__":
    import os
    import json
    from classes import Semester

    save_path = os.path.dirname(os.path.realpath(__file__))
    save_path = fr"{save_path:s}\..\Saves"
    
    names = [name for name in os.listdir(save_path)]
    
    semesters = []

    for name in names:
        with open(f"{save_path}\\{name}", "r") as f:
            data = json.load(f)
            loaded_semester = Semester.from_dict(data)
            semesters.append(loaded_semester)

            # Print loaded data
            print(loaded_semester.show())

    semester1 = semesters[0]
    semester2 = semesters[1]
    
    gpa1 = calculate_gpa(semester1)
    gpa2 = calculate_gpa(semester2)
    
    gpax = calculate_gpax([semester1, semester2])
    
    print(f"GPA Semester 1: {gpa1:.2f}")
    print(f"GPA Semester 2: {gpa2:.2f}")
    print(f"GPAX: {gpax:.2f}")