import mysql.connector as msql

# Get directors by name function
def get_directors_by_name():
    director_name = input("Enter the name of a director or part thereof: ")
    
    # Connect to MySQL
    try: 
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 
        
        # Select the database
        cursor = con.cursor()
    
        # Command to select the data from the table
        sql = """
        SELECT d.DirectorName, f.FilmName, s.StudioName
        FROM director d
        JOIN film f ON d.DirectorID = f.FilmDirectorID
        JOIN studio s ON f.FilmStudioID = s.StudioID
        WHERE d.DirectorName LIKE %s
        """

        #  Execute the command
        cursor.execute(sql, ('%' + director_name + '%',))

        # Fetch the results
        results = cursor.fetchall()

        if results:
            print(f"Film Details for '{director_name}':")
            for row in results:
                print(row)
        else:
            print(f"No results found for '{director_name}'.")
            
    except msql.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        con.close()
