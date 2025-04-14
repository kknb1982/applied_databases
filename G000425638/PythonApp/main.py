from menu import menu
from menu1_directors import get_directors_by_name
from menu2_actor_by_dob import get_birth_month, get_actor_by_month
from menu3_new_actor import check_actor_ID
import mysql.connector as msql

def menu():
    options = "MENU \n 1 - View Directors & Film \n 2 - View Actors by Month of Birth \n 3 - Add New Actor \n 4 - View Married Actors \n 5 - Add Actor Marriage \n 6. View Studios \n x - Exit Application"
    print(options)
    choice = input("Choose a menu option: ")
    
    if choice == "1":
        get_directors_by_name()
        menu()
    
    elif choice == "2":
        month_num = get_birth_month()
        if month_num:
            get_actor_by_month(month_num)
        else:
            print("Invalid month input. Please try again.")
        menu()
    
    elif choice == "3":
        check_actor_ID()
        menu()

if __name__ == "__main__":
    menu()


    

    
    


elif choice == "4":
    view_married_actors()
    
elif choice == "5":
    add_actor_marriage()
    
elif choice == "6":
    view_studios()
elif choice == "x":
    print("Exiting application...")
else:
    print(f"Invalid choice. Please try again. \n{options}")
