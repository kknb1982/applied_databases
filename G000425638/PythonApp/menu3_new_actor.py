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
            value = (actor_id,)  # Wrap value in a tuple
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
            dob = input("Enter Actor Date of Birth (YYYY-MM-DD): ")
        
        gender = input("Enter Actor Gender: ")
        if gender not in ['Male', 'Female', 'M', 'F']:
            while gender not in ['Male', 'Female', 'M', 'F']:
                print("Invalid gender. Please enter 'M', 'F', 'Male', or 'Female'.")
                gender = input("Enter Actor Gender (M/F): ")
            if gender == 'M':
                gender = "Male"
            elif gender == 'F':
                gender = "Female"
                        
        country_id = input("Enter Country ID: ")

        # Connect to the MySQL database
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 

        if con.is_connected():
            cursor = con.cursor()

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

    except Error as e:
        print(f"Database error: {e}")
    except Exception as ex:
        print(f"Error: {ex}")
    finally:
        if con.is_connected():
            cursor.close()
            con.close()


