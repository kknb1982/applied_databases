import mysql.connector as msql

def get_studios():
        
    # Connect to MySQL
    try: 
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 
        
        # Select the database
        cursor = con.cursor()
    
        # Command to select the data from the table
        sql = """
        SELECT StudioName, StudioID
        FROM studio 
        """
        
        #  Execute the command
        cursor.execute(sql)

        # Fetch the results
        results = cursor.fetchall()

        if results:
            print(f"Studio details':")
            for row in results:
                print(row)
        else:
            print(f"No results found.")
            
    except msql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        con.close()