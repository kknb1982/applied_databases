from datetime import datetime
import mysql.connector as msql

def check_actor_ID():
    # Collect the actor ID
    id = input("Enter Actor ID: ")
    
    # Check against the database to see if the ID already exists
    try: 
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 
        
        # Select the database
        cursor = con.cursor()
    
        # Command to select the data from the table
        sql = """
        SELECT * FROM actor WHERE ActorID = %s
        """
        id = int(id)  # Ensure month_num is an integer
        
        #  Execute the command
        cursor.execute(sql, (id,))
        
        results = cursor.fetchall()
        if len(results) == 0:
            print(f"Actor ID {id} does not exist.")
        else:
            print(f"*** ERROR: Actor ID {id} already exists in the database. ***")
            print("Please enter a different ID.")
            return
    except msql.Error as e:
        print("Error connecting to MySQL", e)
    finally:
        # Close the connection
        if con.is_connected():
            cursor.close()
            con.close()
