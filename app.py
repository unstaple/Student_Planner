import datetime as dt
import pandas as pd
from google.oauth2.service_account import Credentials
from source import *
import time

semesters = None
current_semester = None

def menu_prompt() -> str:
    """
    Default menu prompt
    """
    global semesters
    semesters = check_path()
    clear()
    print()
    if semesters:
        for semester in semesters:
            print(semester.show())
    print(f"\nCumulative GPAX : {calculate_gpax([semester.course_data for semester in semesters])}\n")
    print("Which option you wanted to choose?")
    option = input("Select Semester (1) | Add a Semester (2) | Quit (3)\n")

    if option.lower().strip() in ["1", "(1)", "select semester"]:
        edit_semester()

    elif option.lower().strip() in ["2", "(2)", "add another semester"]:
        clear()
        year = input("Input new semester year (20xx) \n")
        clear()
        season = input("Input new semester season (Fall/Summer/etc.)\n")
        clear()
        print("NOTE : IF A FILE WITH THE SAME NAME ALREADY EXIST, THIS ACTION WILL OVERWRITE THE FILE")
        option = input(f"Confirm this semester? -> {year}_{season} (Y/N) --> ")
        clear()
        if option.lower() == "y":
            try:
                new_semester = Semester(year=year, season=season)
                new_semester.to_json()
                semesters.append(new_semester)
                print("\nSemester Added!")
                menu_prompt()
            except Exception as e:
                print(f"Error Occurred : {e}")
                menu_prompt()
        else:
            menu_prompt()

    elif option.lower().strip() in ["3", "(3)", "quit", "q"]:
        clear()
        quit()

    else:
        clear()
        print("Please type a proper option.")
        print("Return to Main Menu in 5 second(s)...")
        time.sleep(5)
        menu_prompt()

def edit_subject():
    pass

def edit_semester():
    global current_semester
    semesters_dict = {}

    clear()

    for i, semester in enumerate(semesters):
        print(f"{i+1} | {semester.info()}")
        semesters_dict[str(i+1)] = semester

    option = input("Please select your semester (Type a number) | Type back to go back to menu | Type quit to exit the program\n")

    if option in semesters_dict:
        current_semester = semesters_dict[option]
        clear()
        print("\n" + semester.show())
        print("Select Class (1) | Add a Class (2) | Edit Semester (3) | Quit (4)")
        option = input()

        if option.lower().strip() in ["1", "(1)", "select semester"]:
            edit_subject()

        elif option.lower().strip() in ["2", "(2)", "add Class", "add a Class"]:
            clear()
            name = input("Input Class name (Calculus 1/Linear algreba/etc.)\n")
            clear()
            try:
                credit = float(input("Input Class credit (3.0/2.0/etc.)\n"))
                clear()
            except ValueError:
                print(f"Value Error, please enter a proper credit")
                edit_semester()
            course_code = input("Input course code (06066303/etc.) (Optional, can be leave blanked)\n")
            if not course_code:
                course_code = None
            clear()
            try:
                subject = Subject(name=name, credit=credit, course_code=course_code)
                current_semester.subjects.append(subject)
                current_semester.to_json()
                print("Successfully added the subject")
                print(subject.show())
                print("Return to Main Menu in 5 second(s)...")
                time.sleep(5)
                menu_prompt()
            except Exception as e:
                print(f"Error Occurred : {e}")
                edit_semester()

        elif option.lower().strip() in ["3", "(3)", "quit"]:
            clear()
            quit()

    elif option.lower() in ["back", "b"]:
        menu_prompt()

    elif option.lower() == ["quit", "q"]:
        clear()
        quit()

    else:
        clear()
        print("Please type a proper option.")
        print("Return to Semester Editing Section in 5 second(s)...")
        time.sleep(5)
        edit_semester()

def main():
    """
    Main loop of the program
    """
    menu_prompt()
    

if __name__ == "__main__":

    main()
