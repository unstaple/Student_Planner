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


def calculate_gpa(course_data):
    """
    Calculate GPA for a semester.
    
    Args:
        course_data (list): List of tuples (score, credit_hours)

    Returns:
        float: GPA value
    """

    thresholds = get_default_thresholds()

    if course_data and thresholds:
        total_grade_points = 0
        total_credits = 0

        for score, credits in course_data:
            grade_point, _ = get_grade_point(score)
            total_grade_points += grade_point * credits
            total_credits += credits

        if total_credits == 0:
            return 0.0
        return total_grade_points / total_credits
    else:
        return 0.0


def calculate_gpax(all_semesters_data):
    """
    Calculate cumulative GPAX across all semesters.
    
    Args:
        all_semesters_data (list): List of semester data, each containing course_data
    
    Returns:
        float: GPAX value
    """
    if all_semesters_data:

        thresholds = get_default_thresholds()

        if all_semesters_data and thresholds:
            total_grade_points = 0
            total_credits = 0

            for semester_data in all_semesters_data:
                for score, credits in semester_data:
                    grade_point, _ = get_grade_point(score)
                    total_grade_points += grade_point * credits
                    total_credits += credits

            if total_credits == 0:
                return 0.0
            return total_grade_points / total_credits
    else:
        return 0.0

if __name__ == "__main__":
    
    # Example: Semester 1 courses (score, credit_hours)
    semester1 = [
        (85, 3),  # 85% in 3-credit course
        (78, 2),  # 78% in 2-credit course
        (92, 4),  # 92% in 4-credit course
    ]
    
    semester2 = [
        (73, 3),
        (68, 2),
        (81, 4),
    ]
    
    gpa1 = calculate_gpa(semester1)
    gpa2 = calculate_gpa(semester2)
    
    gpax = calculate_gpax([semester1, semester2])
    
    print(f"GPA Semester 1: {gpa1:.2f}")
    print(f"GPA Semester 2: {gpa2:.2f}")
    print(f"GPAX: {gpax:.2f}")