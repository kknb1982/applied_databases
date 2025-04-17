import mysql.connector as msql

# Create a cache
studio_cache = None

def get_studios():
    global studio_cache
    # Check if the cache is empty
    if studio_cache is not None:
        print("Using cached data.")
        for studio in studio_cache:
            print(studio)
        return

# First time access — query from DB and cache
    # Connect to MySQL
    try: 
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 
        
        # Select the database
        cursor = con.cursor()
    
        # Command to select the data from the table
        sql = """
        SELECT StudioID, StudioName
        FROM studio 
        ORDER BY StudioID ASC
        """
        
        #  Execute the command
        cursor.execute(sql)

        # Fetch the results
        studio_cache = cursor.fetchall()
        print(f"Studio details':")
        for studio in studio_cache:
            print(studio)

    except msql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        con.close()
        
get_studios()
