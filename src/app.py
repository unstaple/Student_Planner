# app.py

try:
    from .source import *
except Exception:
    from source import *

from typing import Optional, Dict, List
import time
import os

PRINT_SECTION_SPACES_VALUES = 0


def print_section(section: str) -> None:
    """Print a boxed section title."""
    border = "-" * (30 + len(section))
    spaces_value = " " * PRINT_SECTION_SPACES_VALUES
    middle = f"|{' ' * 14}{section}{' ' * 14}|"
    print(f"{spaces_value}{border}")
    print(f"{spaces_value}{'|' + ' ' * (len(border) - 2) + '|'}")
    print(f"{spaces_value}{middle}")
    print(f"{spaces_value}{'|' + ' ' * (len(border) - 2) + '|'}")
    print(f"{spaces_value}{border}\n")


def prompt_choice(raw: str, valid_map: Dict[str, List[str]]) -> str:
    """
    Normalize input and map to canonical key.
    Returns canonical key or empty string if not matched.
    """
    opt = raw.lower().strip()
    for key, synonyms in valid_map.items():
        if opt in synonyms:
            return key
    return ""


def confirm(title: str, data: str) -> bool:
    """Simple yes/no confirm prompt."""
    res = input(f"Confirm {title}?\n{data} (Y/N) --> ").lower().strip()
    return res in ("y", "yes")

def find_semester_for_subject(subject: Subject, semesters: List[Semester]) -> Optional[Semester]:
    for s in semesters:
        if subject in s.subjects:
            return s
    return None


# ---------------- Main loop & top-level menus ---------------- #

def main_loop():
    """Main loop that repeatedly shows the top menu."""
    while True:
        clear()
        semesters = check_path()
        print_section("Main Menu")
        if semesters:
            for s in semesters:
                print("\n# ---------------- Semester Break ---------------- #\n")
                print(s.show())
        gpax = calculate_gpax(semesters)
        print()
        print_section(f"Cumulative GPAX : {gpax:.2f}")
        print("\nWhich option you wanted to choose?\n")
        raw = input("Select Semester (1) | Add a Semester (2) | Check Deadline (3) | Quit (4)\n")
        choice = prompt_choice(raw, {
            "select_semester": ["1", "(1)", "select semester", "select"],
            "add_semester": ["2", "(2)", "add another semester", "add another", "add semester", "add"],
            "check_deadline": ["3", "(3)", "check deadline", "check"],
            "quit": ["4", "(4)", "quit", "q"]
        })

        if choice == "select_semester":
            semester_menu(semesters)
        elif choice == "add_semester":
            add_semester_flow(semesters)
        elif choice == "check_deadline":
            clear()
            deadline_report(semesters)
            sub = input("Type anything to return to Main Menu | Quit (q)\n").lower().strip()
            if sub in ("q", "quit"):
                clear()
                return
        elif choice == "quit":
            clear()
            return
        else:
            clear()
            print("Please type a proper option. Returning to Main Menu in 3 seconds...")
            time.sleep(3)


# ---------------- Semester-level flows ---------------- #

def add_semester_flow(semesters: List[Semester]) -> None:
    clear()
    year = input("Input new semester year (20xx) \n").strip()
    clear()
    season = input("Input new semester season (Fall/Summer/etc.)\n").strip()
    clear()
    print("NOTE : IF A FILE WITH THE SAME NAME ALREADY EXIST, THIS ACTION WILL OVERWRITE THE FILE")
    if not confirm("Semester", f"{year}_{season}"):
        print("Canceled semester adding, returning to Main Menu in 3 seconds...")
        time.sleep(3)
        return
    try:
        new_semester = Semester(year=year, season=season)
        new_semester.to_json()
        semesters.append(new_semester)
        print("\nSemester Added! Returning to Main Menu in 3 seconds...")
    except Exception as e:
        print(f"Error Occurred : {e}")
    time.sleep(3)

def delete_semester(semester: Optional[Semester], semesters: List[Semester]) -> None:
    clear()
    if not confirm("Semester Deletion", f"{semester.year}_{semester.season}"):
        print("Canceled Semester Deletion.")
        time.sleep(3)
        return
    try:
        if hasattr(semester, "delete"):
            # attempt to delete file if path exists
            try:
                semester.delete()
            except Exception:
                # fallback: try to remove using filename convention
                pass
        else:
            # fallback removal using filename
            _dir_path = os.path.dirname(os.path.realpath(__file__))
            _save_dir_path = os.path.join(_dir_path, "..", "Saves")
            filename = f"{semester.year}_{semester.season}.json"
            filepath = os.path.join(_save_dir_path, filename)
            if os.path.exists(filepath):
                os.remove(filepath)

                # remove from in-memory list if found
                if semester in semesters:
                    semesters.remove(semester)

        print("Semester deleted. Returning to Main Menu...")
    except Exception as e:
        print(f"Error deleting semester: {e}")
    time.sleep(3)


def semester_menu(semesters: List[Semester]) -> None:
    """Choose a semester and operate on it."""
    if not semesters:
        print("No semesters available. Returning to Main Menu...")
        time.sleep(3)
        return

    current = semester_selection_menu(semesters=semesters)

    # semester operations loop
    while True:
        clear()
        print_section("Semester Menu")
        print(current.show() +"\n")
        raw = input("Select Class (1) | Add a Class (2) | Edit Semester (3) | Back to Main Menu (4) | Quit (5)\n").lower().strip()
        opt = prompt_choice(raw, {
            "select_class": ["1", "(1)", "select class"],
            "add_class": ["2", "(2)", "add class", "add a class"],
            "edit_semester": ["3", "(3)", "edit semester"],
            "back": ["4", "(4)", "back", "b"],
            "quit": ["5", "(5)", "quit", "q"]
        })
        
        match opt:

            case "select_class":
                subject = subject_selection_menu(current)
                if subject:
                    subject_menu(subject, current, semesters)

            case "add_class":
                subject_adding_menu(current)

            case "edit_semester":
                semester_edit_menu(current, semesters)
                # if semester was deleted, return to main menu
                if current not in check_path():
                    return

            case "back":
                return

            case "quit":
                clear()
                exit(0)

            case _:
                print("Please type a proper option.")
                time.sleep(3)

def semester_selection_menu(semesters: List[Semester]) -> Optional[Semester]:
    """Let user pick a semester."""
    while True:
        clear()
        print_section("Semester Selection")

        for i, sem in enumerate(semesters, start=1):
            print(f"{i} | {sem.info().strip()}\n")

        opt = input("Please select your semester (Type a number) | Type back to go back to menu | Type quit to exit the program\n").lower().strip()

        if opt in [str(i) for i in range(1, len(semesters) + 1)]:
            current = semesters[int(opt) - 1]
            return current

        if opt in ("back", "b"):
            return

        if opt in ("quit", "q"):
            clear()
            exit(0)
        print("Please type a proper option.")
        time.sleep(3)

def semester_edit_menu(semester: Semester, semesters: List[Semester]) -> None:
    clear()
    print_section("Edit Semester")
    print(semester.show() + "\n")
    raw = input("Edit Year (1) | Edit Season (2) | Delete Semester (3) | Back (4) | Quit (5)\n").lower().strip()
    opt = prompt_choice(raw, {
            "edit_year": ["1", "(1)", "edit year"],
            "edit_season": ["2", "(2)", "edit season"],
            "delete_semester": ["3", "(3)", "delete semester"],
            "back": ["4", "(4)", "back", "b"],
            "quit": ["5", "(5)", "quit", "q"]
        })

    match opt:
        case "edit_year":
            clear()
            new_year = input("Enter new year (20xx):\n").strip()
            if confirm("Semester Year Editing", f"{semester.year}(Old) --> {new_year}(New)"):
                try:
                    if hasattr(semester, "delete"):
                    # attempt to delete file if path exists
                        try:
                            semester.delete()
                        except Exception:
                            # fallback: try to remove using filename convention
                            pass
                    else:
                        # fallback removal using filename
                        _dir_path = os.path.dirname(os.path.realpath(__file__))
                        _save_dir_path = os.path.join(_dir_path, "..", "Saves")
                        filename = f"{semester.year}_{semester.season}.json"
                        filepath = os.path.join(_save_dir_path, filename)
                        if os.path.exists(filepath):
                            os.remove(filepath)
                            # remove from in-memory list if found
                            if semester in semesters:
                                semesters.remove(semester)

                except Exception as e:
                    print(f"Error deleting semester: {e}")
                    time.sleep(3)

                semester.year = new_year
                semester.to_json()
                semesters.append(semester)
                print("Successfully updated the semester season.")
            else:
                print("Canceled.")
                time.sleep(3)
                return
            return

        case "edit_season":
            clear()
            new_season = input("Enter new season (Fall/Summer/etc.):\n").strip()
            if confirm("Semester Season Editing", f"{semester.season}(Old) --> {new_season}(New)"):
                try:
                    if hasattr(semester, "delete"):
                    # attempt to delete file if path exists
                        try:
                            semester.delete()
                        except Exception:
                            # fallback: try to remove using filename convention
                            pass
                    else:
                        # fallback removal using filename
                        _dir_path = os.path.dirname(os.path.realpath(__file__))
                        _save_dir_path = os.path.join(_dir_path, "..", "Saves")
                        filename = f"{semester.year}_{semester.season}.json"
                        filepath = os.path.join(_save_dir_path, filename)
                        if os.path.exists(filepath):
                            os.remove(filepath)
                            # remove from in-memory list if found
                            if semester in semesters:
                                semesters.remove(semester)

                except Exception as e:
                    print(f"Error deleting semester: {e}")
                    time.sleep(3)

                semester.season = new_season
                semester.to_json()
                semesters.append(semester)
                print("Successfully updated the semester season.")
            else:
                print("Canceled.")
                time.sleep(3)
                return

        case "delete_semester":
            delete_semester(semester=semester, semesters=semesters)
            return

        case "back":
            return
    
        case "quit":
            clear()
            quit(0)

        case _:
            clear()
            print("Please type a proper option.")
            time.sleep(3)
            return


# ---------------- Subject-level flows ---------------- #

def subject_selection_menu(semester: Semester) -> Optional[Subject]:
    """Let user pick a subject inside a semester."""
    if not semester.subjects:
        print("No subjects in this semester.")
        time.sleep(3)
        return None

    while True:
        clear()
        print_section("Class Selection")
        for i, subj in enumerate(semester.subjects, start=1):
            print(f"{i} | {subj.info().strip()}\n")
        opt = input("Please select your class (Type a number) | Type back to go back | Type quit to exit\n").lower().strip()
        if opt in [str(i) for i in range(1, len(semester.subjects) + 1)]:
            return semester.subjects[int(opt) - 1]
        if opt in ("back", "b"):
            return None
        if opt in ("quit", "q"):
            clear()
            exit(0)
        print("Please type a proper option.")
        time.sleep(3)


def subject_adding_menu(semester: Semester) -> None:
    clear()
    name = input("Input Class name (Calculus 1/Linear algebra/etc.)\n").strip()
    clear()
    try:
        credit = float(input("Input Class credit (3.0/2.0/etc.)\n").strip())
    except ValueError:
        print("Value Error, please enter a proper credit")
        time.sleep(3)
        return
    clear()
    course_code = input("Input course code (06066303/etc.) (Optional, leave blank)\n").strip() or None

    try:
        subject = Subject(name=name, credit=credit, course_code=course_code)
        semester.subjects.append(subject)
        semester.to_json()
        print("Successfully added the subject")
        print(subject.show().replace("No Current Assignment", "").strip())
    except Exception as e:
        print(f"Error Occurred : {e}")
    time.sleep(3)


def subject_menu(subject: Subject, semester: Semester, semesters: List[Semester]) -> None:
    """Operations for a single subject."""
    while True:
        clear()
        print_section("Class Menu")
        print(subject.show() + "\n")
        raw = input("Select Assignment (1) | Add Assignment (2) | Edit Class (3) | Delete Class (4) | Back to Semester Menu (5)\n").lower().strip()
        choice = prompt_choice(raw, {
            "select_assignment": ["1", "(1)", "select assignment"],
            "add_assignment": ["2", "(2)", "add assignment"],
            "edit_class": ["3", "(3)", "edit class"],
            "delete_class": ["4", "(4)", "delete class"],
            "back": ["5", "(5)", "back", "b"]
        })
        
        match choice:

            case "select_assignment":
                if not subject.assignments:
                    print("No assignments in this class. Returning...")
                    time.sleep(3)
                    return
                assignment = assignment_selection_menu(subject)
                if assignment:
                    assignment_edit_menu(assignment, subject, semester)
            case "add_assignment":
                assignment_adding_menu(subject, semester)
            case "edit_class":
                subject_edit_menu(subject, semesters)
            case "delete_class":
                if not confirm("Class Deletion", f"{subject.name} | Credit : {subject.credit}"):
                    print("Canceled.")
                    time.sleep(3)
                    continue
                try:
                    semester.subjects.remove(subject)
                    semester.to_json()
                    print("Successfully deleted the class.")
                except Exception as e:
                    print(f"Error occurred while deleting: {e}")
                time.sleep(3)
                return
            case "back":
                return
            case _:
                print("Invalid option.")
                time.sleep(3)


# ---------------- Assignment-level flows ---------------- #

def assignment_selection_menu(subject: Subject) -> Optional[Assignment]:
    if not subject.assignments:
        return None
    while True:
        clear()
        print_section("Select Assignment")
        for i, a in enumerate(subject.assignments, start=1):
            print(f"{i} | {a.name} | Score : {a.current_score}/{a.max_score} | Status : {a.status} | Due : {a.deadline}")
        opt = input("Please select your assignment (Type a number) | Type back to go back | Type quit to exit\n").lower().strip()

        if opt in [str(i) for i in range(1, len(subject.assignments) + 1)]:
            return subject.assignments[int(opt) - 1]

        if opt in ("back", "b"):
            return None

        if opt in ("quit", "q"):
            clear()
            exit(0)

        print("Invalid option. Try again.")
        time.sleep(3)


def assignment_adding_menu(subject: Subject, semester: Semester) -> None:
    clear()
    name = input("Input Assignment name:\n").strip()
    try:
        max_score = float(input("Input Maximum score for this assignment (e.g. 15):\n").strip())
    except ValueError:
        print("Invalid max score. Returning to Class Menu...")
        time.sleep(3)
        return

    print("Input deadline in format : MM/DD/YY HH:MM:SS (e.g. 10/03/25 13:55:26). Leave blank for no deadline.")
    deadline = input("Deadline: ").strip() or None

    try:
        new_assign = Assignment(name=name, max_score=max_score, deadline=deadline)
        subject.assignments.append(new_assign)
        semester.to_json()
        print("Successfully added assignment.")
        print(new_assign.show())
    except Exception as e:
        print(f"Error occurred while adding assignment: {e}")
    time.sleep(3)


def assignment_edit_menu(assignment: Assignment, subject: Subject, semester: Semester) -> None:
    """Looped assignment editor; returns when user chooses back."""
    while True:
        clear()
        print_section("Assignment Menu")
        print(assignment.show())
        raw = input("Edit Name (1) | Edit Max Score (2) | Edit Current Score (3) | Edit Deadline (4) | Toggle Done (5) | Delete Assignment (6) | Back (7) | Return to Main Menu (8) | Quit (9)\n").lower().strip()
        opt = choice = prompt_choice(raw, {
            "edit_name": ["1", "(1)", "edit name"],
            "edit_max_score": ["2", "(2)", "edit max score"],
            "edit_current_score": ["3", "(3)", "edit current score"],
            "edit_deadline": ["4", "(4)", "edit deadline"],
            "toggle_done": ["5", "(5)", "toggle done"],
            "delete_assignment": ["6", "(6)", "delete assignment"],
            "back": ["7", "(7)", "back", "b"],
            "quit": ["8", "(8)", "quit", "q"],
        })
        
        
        match opt:
            case "edit_name":
                new_name = input("Please enter new assignment name:\n").strip()
                if confirm("Assignment Name Editing", f"{assignment.name}(Old) --> {new_name}(New)"):
                    assignment.name = new_name
                    semester.to_json()
                    print("Successfully changed the assignment name.")
                else:
                    print("Canceled.")
                time.sleep(3)

            case "edit_max_score":
                try:
                    new_max = float(input("Please enter new max score:\n").strip())
                except ValueError:
                    print("Invalid number.")
                    time.sleep(3)
                    continue
                if confirm("Assignment Max Score Editing", f"{assignment.max_score}(Old) --> {new_max}(New)"):
                    assignment.max_score = new_max
                    semester.to_json()
                    print("Successfully changed the max score.")
                else:
                    print("Canceled.")
                time.sleep(3)

            case "edit_current_score":
                try:
                    new_score = float(input("Please enter current score (use exact number):\n").strip())
                except ValueError:
                    print("Invalid number.")
                    time.sleep(3)
                    continue
                if confirm("Assignment Current Score Editing", f"{assignment.current_score}(Old) --> {new_score}(New)"):
                    assignment.current_score = new_score
                    assignment.isDone = True
                    semester.to_json()
                    print("Successfully changed the current score and marked as done.")
                else:
                    print("Canceled.")
                time.sleep(3)

            case "edit_deadline":
                print("Input deadline in format : MM/DD/YY HH:MM:SS (e.g. 10/03/25 13:55:26). Leave blank to unset.")
                new_deadline = input("New Deadline: ").strip() or None
                if confirm("Assignment Deadline Editing", f"{assignment.deadline}(Old) --> {new_deadline}(New)"):
                    assignment.deadline = new_deadline
                    semester.to_json()
                    print("Successfully changed the deadline.")
                else:
                    print("Canceled.")
                time.sleep(3)

            case "toggle_done":
                assignment.isDone = not assignment.isDone
                if assignment.isDone and assignment.current_score == 0:
                    try:
                        new_score = input("Enter score achieved (or leave blank to keep 0):\n").strip()
                        new_score = float(new_score) if new_score != "" else 0.0
                    except ValueError:
                        new_score = 0.0
                    assignment.current_score = new_score
                semester.to_json()
                print(f"Toggled done -> {assignment.isDone}.")
                time.sleep(3)

            case "delete_assignment":
                if confirm("Assignment Deletion", f"{assignment.name} | Score : {assignment.current_score}/{assignment.max_score}"):
                    try:
                        subject.assignments.remove(assignment)
                        semester.to_json()
                        print("Successfully deleted assignment.")
                        time.sleep(3)
                        return
                    except Exception as e:
                        print(f"Error deleting assignment: {e}")
                        time.sleep(3)
                else:
                    print("Canceled.")
                    time.sleep(3)

            case "back":
                return

            case "quit":
                clear()
                quit(0)

            case _:
                print("Please type a proper option.")
                time.sleep(3)


def subject_edit_menu(subject: Subject, semesters: List[Semester]) -> None:
    """Edit subject metadata"""
    clear()
    raw = input("Edit Course Code (1) | Edit Course Name (2) | Edit Credit (3) | Back (4)\n").lower().strip()
    opt = prompt_choice(raw, {
        "edit_course_code": ["1", "(1)", "edit course code"],
        "edit_course_name": ["2", "(2)", "edit course name"],
        "edit_credit": ["3", "(3)", "edit credit"],
        "back": ["4", "(4)", "back", "b"],
        "quit": ["5", "(5)", "quit", "q"]
        })
    

    match opt:
        case "edit_course_code":
            new_course_code = input("Please enter new Class's Course Code.\n").strip()
            if confirm("Class's Course Code Editing", f"{subject.course_code}(Old Course Code) --> {new_course_code}(New Course Code)"):
                subject.course_code = new_course_code
                semester = find_semester_for_subject(subject, semesters)
                if semester:
                    semester.to_json()
                print("Successfully changed the Class's Course code.")
            else:
                print("Canceled Course Code Editing.")
            time.sleep(3)
            return

        case "edit_course_name":
            new_name = input("Please enter a new Name.\n").strip()
            if confirm("Class's Name Editing", f"{subject.name}(Old Name) --> {new_name}(New Name)"):
                subject.name = new_name
                semester = find_semester_for_subject(subject, semesters)
                if semester:
                    semester.to_json()
                print("Successfully changed the Class's Name.")
            else:
                print("Canceled Class's Name.")
            time.sleep(3)
            return

        case "edit_credit":
            new_credit_raw = input("Please enter a new Course Credit.\n").strip()
            try:
                new_credit = float(new_credit_raw)
            except ValueError:
                print("Invalid credit.")
                time.sleep(3)
                return
            if confirm("Class's Credit Editing", f"{subject.credit}(Old Credit) --> {new_credit}(New Credit)"):
                subject.credit = new_credit
                semester = find_semester_for_subject(subject, semesters)
                if semester:
                    semester.to_json()
                print("Successfully changed the Class's Credit.")
            else:
                print("Canceled Class's Credit Editing.")
            time.sleep(3)
            return

        case "back":
            return

        case "quit":
            clear()
            quit(0)

        case _:
            print("Please type a proper option.")
            time.sleep(3)
            return

# ---------------- Entrypoint ---------------- #

def main():
    try:
        main_loop()
    except KeyboardInterrupt:
        clear()
        print("\nExiting...")

if __name__ == "__main__":
    print("Program Started...")
    print("Saves directory:", saves_dir())
    time.sleep(3)
    main()
