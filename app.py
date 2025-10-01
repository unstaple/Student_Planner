from google.oauth2.service_account import Credentials
from source import *
import time

semesters = None
PRINT_SECTION_SPACES_VALUES = 0

def print_section(section):
    border = "-"*15 + "-"*len(section) + "-"*15
    spaces = "|" + " "*(len(border)-2) + "|"
    middle = "|" + " "*14 + section + " "*14 + "|"
    spaces_value = " "*PRINT_SECTION_SPACES_VALUES
    print(f"{spaces_value}{border}")
    print(f"{spaces_value}{spaces}")
    print(f"{spaces_value}{middle}")
    print(f"{spaces_value}{spaces}")
    print(f"{spaces_value}{border}\n")

def main_menu() -> str:
    """
    Default menu prompt
    """
    global semesters
    semesters = check_path()
    clear()
    print_section("Main Menu")
    if semesters:
        for semester in semesters:
            print(semester.show())
    # guard in case semesters is empty or check_path returned None
    gpax = calculate_gpax(semesters)
    print_section(f"Cumulative GPAX : {gpax}")
    print("\nWhich option you wanted to choose?\n")
    option = input("Select Semester (1) | Add a Semester (2) | Check Deadline (3) | Quit (4)\n")
    opt = option.lower().strip()

    match opt:
        case "1" | "(1)" | "select semester":
            semester_menu()

        case "2" | "(2)" | "add another semester" | "add another" | "add semester":
            clear()
            year = input("Input new semester year (20xx) \n")
            clear()
            season = input("Input new semester season (Fall/Summer/etc.)\n")
            clear()
            print("NOTE : IF A FILE WITH THE SAME NAME ALREADY EXIST, THIS ACTION WILL OVERWRITE THE FILE")
            confirm = input(f"Confirm this semester? -> {year}_{season} (Y/N) --> ").lower().strip()
            clear()
            if confirm == "y":
                try:
                    new_semester = Semester(year=year, season=season)
                    new_semester.to_json()
                    semesters.append(new_semester)
                    print("\nSemester Added!")
                    main_menu()
                except Exception as e:
                    print(f"Error Occurred : {e}")
                    main_menu()
            else:
                print("Canceled semester adding, returning to Main Menu in 3 seconds...")
                time.sleep(3)
                main_menu()

        case "3" | "(3)" | "check deadline" | "check":
            deadline_menu()

        case "4" | "(4)" | "quit" | "q":
            clear()
            quit()

        case _:
            clear()
            print("Please type a proper option.")
            print("Return to Main Menu in 3 second(s)...")
            time.sleep(3)
            main_menu()

def deadline_menu():
    clear()
    deadline_report(semesters)
    opt = input("Type anything to return to Main Menu | Quit (q)\n").lower().strip()
    
    match opt:

        case "quit" | "q":
            clear()
            quit()

        case _:
            main_menu()

def semester_menu():
    current_semester = semester_selection()
    clear()
    print_section("Semester Menu")
    print("\n" + current_semester.show())
    inner_opt = input("Select Class (1) | Add a Class (2) | Edit Semester (3) | Back to Main Menu (4) | Quit (5)\n").lower().strip()

    match inner_opt:
        case "1" | "(1)" | "select class":
            subject_edit_menu()

        case "2" | "(2)" | "add class" | "add a class":
            subject_adding_menu(current_semester)

        case "3" | "(3)" | "edit semester":
            semester_edit_menu(current_semester)
            
        case "4" | "(4)" | "back" | "b":
            main_menu()

        case "5" | "(5)" | "quit" | "q":
            clear()
            quit()

        case _:
            clear()
            print("Please type a proper option.")
            print("Return to Semester Editing Section in 3 second(s)...")
            time.sleep(3)
            semester_menu()

def semester_selection():
    """
    Semester selection function
    
    Returns:
        object: semester object
    """
    
    global semesters
    semesters_dict = {}
    clear()

    for i, semester in enumerate(semesters):
        print(f"{i+1} | {semester.info()}")
        semesters_dict[str(i+1)] = semester

    opt = input("Please select your semester (Type a number) | Type back to go back to menu | Type quit to exit the program\n").lower().strip()

    if opt in semesters_dict:
        return semesters_dict[opt]

    elif opt in ["back", "b"]:
        main_menu()

    elif opt in ["quit", "q"]:
        clear()
        quit()

    else:
        clear()
        print("Please type a proper option.")
        print("Return to Semester Editing Section in 3 second(s)...")
        time.sleep(3)
        semester_menu()
            
def subject_selection_menu(semester):
    subject_dict = {}
    for i, subject in enumerate(semester.subjects):
        print(f"{i+1} | {subject.info()}")
        subject_dict[str(i+1)] = subject

def subject_adding_menu(semester):
    clear()
    name = input("Input Class name (Calculus 1/Linear algebra/etc.)\n")
    clear()
    try:
        credit = float(input("Input Class credit (3.0/2.0/etc.)\n"))
        clear()
    except ValueError:
        print("Value Error, please enter a proper credit")
        print("Return to Semester Editing Section in 3 second(s)...")
        time.sleep(3)
        semester_menu()
        return
    course_code = input("Input course code (06066303/etc.) (Optional, can be leave blanked)\n")
    if not course_code:
        course_code = None
    clear()
    try:
        subject = Subject(name=name, credit=credit, course_code=course_code)
        semester.subjects.append(subject)
        semester.to_json()
        print("Successfully added the subject")
        print(subject.show())
        print("Return to Main Menu in 3 second(s)...")
        time.sleep(3)
        main_menu()
    except Exception as e:
        print(f"Error Occurred : {e}")
        semester_menu()

def confirm(confirming_text, data):
    """
    Confirming function
    
    Args:
        confirming_text (str): Thing that user wanted to confirm eg. Class or Semester
        data (str): Data that the user wanted to add or edit
    
    Returns:
        bool: confirm status from the user
    """

    return True if input(f"Confirm this {confirming_text}?\n{data} (Y/N) --> ").lower().strip() in ["y", "yes"] else False

def subject_menu(semester):
    clear()
    # wait for imprement

def subject_edit_menu(subject):
    clear()
    opt = input("Edit Course Code (1) | Edit Course Name (2) | Edit Credit (3)\n").lower().strip()
    
    match opt:
        case "1" | "(1)" | "edit course code":
            new_course_code = input("Please enter new Class\'s Course Code.\n")

            if confirm("Class\'s Course Code Editing", f"{subject.course_code}(Old Course Code) --> {new_course_code}(New Course Code)"):
                subject.course_code = new_course_code
                print("Successfully changed the Class\'s Course code.")
                print(subject.show())
                print("Return to Main Menu in 3 second(s)...")
                time.sleep(3)
                main_menu()
            else:
                print("Canceled Class\'s Course Code Editing Section.")
                print("Return to Main Menu in 3 second(s)...")
                time.sleep(3)
                main_menu()

        case "2" | "(2)" | "edit course name":
            new_name = input("Please enter a new Name.\n")
    
            if confirm("Class\'s Name Editing", f"{subject.name}(Old Name) --> {new_name}(New Name)"):
                subject.name = new_name
                print("Successfully changed the Class\'s Name.")
                print(subject.show())
                print("Return to Main Menu in 3 second(s)...")
                time.sleep(3)
                main_menu()
            else:
                print("Canceled Class\'s Name Editing Section.")
                print("Return to Main Menu in 3 second(s)...")
                time.sleep(3)
                main_menu()

        case "3" | "(3)" | "edit credit":
            new_credit = input("Please enter a new Course Credit.\n")
            if confirm("Class\'s Credit Editing", f"{subject.credit}(Old Credit) --> {new_credit}(New Credit)"):
                subject.credit = new_credit
                print("Successfully changed the Class\'s Credit.")
                print(subject.show())
                print("Return to Main Menu in 3 second(s)...")
                time.sleep(3)
                main_menu()
            else:
                print("Canceled Class\'s Credit Editing Section.")
                print("Return to Main Menu in 3 second(s)...")
                time.sleep(3)
                main_menu()
        case _:
            clear()
            print("Please type a proper option.")
            print("Return to Class Editing Section in 3 second(s)...")
            time.sleep(3)
            subject_edit_menu()

def semester_edit_menu(semester):
    clear()
    # waiting for imprement

def main():
    """
    Main loop of the program
    """
    main_menu()
    

if __name__ == "__main__":

    main()
