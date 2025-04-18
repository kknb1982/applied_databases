from datetime import datetime
import mysql.connector as msql

import mysql.connector as msql
from mysql.connector import Error

def add_actor():
    try:
        # Collect user input
        actor_id = input("Enter Actor ID: ")
        
        # Connect to the MySQL database
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 

        if con.is_connected():
            cursor = con.cursor()

            # Check if actor ID already exists
            sql = "SELECT * FROM actor WHERE ActorID = %s"
            value = (actor_id,)  
            cursor.execute(sql, value)
            if cursor.fetchone():
                print(f"Error: Actor ID {actor_id} already exists.")
                return

            name = input("Enter Actor Name: ")
            dob = input("Enter Actor Date of Birth (YYYY-MM-DD): ")
        
            # Validate date format
            try:
                datetime.strptime(dob, '%Y-%m-%d')
            except ValueError:
                print("Incorrect date format, should be YYYY-MM-DD")
                return
        
            gender = input("Enter Actor Gender: ").strip()
            while gender not in ['Male', 'Female', 'M', 'F']:
                print("Invalid gender. Please enter 'M', 'F', 'Male', or 'Female'.")
                gender = input("Enter Actor Gender (M/F): ")
            
            gender = "Male" if gender in ['M', 'Male'] else "Female"

            country_id = input("Enter Country ID: ")

            # Check if country ID exists
            cursor.execute("SELECT * FROM country WHERE CountryID = %s", (country_id,))
            if not cursor.fetchone():
                print(f"Error: Country ID {country_id} does not exist.")
                return

            # Insert actor into the Actor table
            insert_query = """
            INSERT INTO Actor (ActorID, ActorName, ActorDOB, ActorGender, ActorCountryID)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (actor_id, name, dob, gender, country_id))
            con.commit()
            print("Actor added successfully!")
            
            ## Retrieve the new actor's ID from the database
            sql = "SELECT * FROM actor WHERE ActorID = %s"
            value = (actor_id,)  
            cursor.execute(sql, value)
            new_actor = cursor.fetchone()
            
            if new_actor:
                print(f"New Actor Record: ")
                print(f"Actor ID: {new_actor[0]}")
                print(f"Actor Name: {name}")
                print(f"Actor DOB: {dob}")
                print(f"Actor gender: {gender}")
                print(f"Actor Country ID: {country_id}")
            else:   
                print(f"Error: Actor ID {actor_id} not found in the database.")
    
    except Error as e:
        print(f"Database error: {e}")
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


