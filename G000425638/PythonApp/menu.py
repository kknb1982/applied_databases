from menu1_directors import get_directors_by_name
from menu2_actor_by_dob import get_birth_month, get_actor_by_month
from menu3_new_actor import add_actor
from menu4_married import check_marriage
from menu5_add_marriage import check_actor_exists, is_actor_married, was_divorced, get_valid_actor, create_marriage
from menu6_studios import get_studios


import mysql.connector as msql
from mysql.connector import Error
from datetime import datetime
from neo4j import GraphDatabase

con = None
driver = None

# Create the options menu
def menu():
    while True:
        options = "MENU \n 1 - View Directors & Film \n 2 - View Actors by Month of Birth \n 3 - Add New Actor \n 4 - View Married Actors \n 5 - Add Actor Marriage \n 6 - View Studios \n x - Exit Application"
        print(options)
        choice = input("Choose a menu option: ")
    
        if choice == "1":
            get_directors_by_name()
    
        elif choice == "2":
            month_num = get_birth_month()
            if month_num:
                get_actor_by_month(month_num)
    
        elif choice == "3":
            add_actor()
        
        elif choice == "4":
            check_marriage()
        
        elif choice == "5": 
            user_input = input("Enter the Actor ID to check for marriages: ")
            check_marriage(user_input)
    
            actor1id = get_valid_actor("Enter Actor 1 ID: ")
            actor2id = get_valid_actor("Enter Actor 2 ID: ")

            married1 = is_actor_married(actor1id)
            married2 = is_actor_married(actor2id)

            divorced1 = was_divorced(actor1id)
            divorced2 = was_divorced(actor2id)

            errors = []

            if married1 and not divorced1:
                errors.append(f"Actor {actor1id} is already married and hasn't been divorced.")
            if married2 and not divorced2:
                errors.append(f"Actor {actor2id} is already married and hasn't been divorced.")
                menu()
        
        elif choice == "6":
            get_studios()
            
        elif choice == "x":
            print("Exiting application...")
            break
        
        else:
            print(f"Invalid choice. Please try again.")