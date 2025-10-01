# Grade calculation functions

def get_default_thresholds():
    """
    Return default grade thresholds.
    
    Returns:
        dict: Default grade thresholds
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

def get_grade_point(score):
    """
    Convert raw score to grade point based on thresholds.
    
    Args:
        score (float): Raw score
        thresholds (dict): Grade thresholds {grade: min_score}
    
    Returns:
        tuple: (grade_point, letter_grade)
    """

    thresholds = get_default_thresholds()
    if score:
        for grade, min_score in sorted(thresholds.items(), key=lambda x: x[1], reverse=True):
            if score >= min_score:
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
                return grade_points[grade], grade
        return (0.0, 'F')  # Default to F if no threshold matches
    else:
        return (0.0, 'F')


def calculate_gpa(semester):
    """
    Calculate GPA for a semester.
    
    Args:
        semester (object): a semester object

    Returns:
        float: GPA value
    """

    total_grade_points = 0
    total_credits = 0

    for subject in semester.subjects:
        grade_point, _ = get_grade_point(subject.score)
        total_grade_points += grade_point * subject.credit
        total_credits += subject.credit

    if total_credits == 0:
        return 0.0

    return total_grade_points / total_credits


def calculate_gpax(all_semester):
    """
    Calculate cumulative GPAX across all semesters.
    
    Args:
        all_semester (list): List of semester, each containing semester object
    
    Returns:
        float: GPAX value
    """
    thresholds = get_default_thresholds()

    if all_semester and thresholds:
        total_grade_points = 0
        total_credits = 0

        for semester in all_semester:
            for subject in semester.subjects:
                grade_point, _ = get_grade_point(subject.score)
                total_grade_points += grade_point * subject.credit
                total_credits += subject.credit

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