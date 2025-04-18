import mysql.connector as msql
# Get birth month function - This checks the input of the month against a dictioonary of months and returns the month number.
def get_birth_month():
    month_lookup = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
        'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }

    input_month = input("Enter the month of birth you are interested in (1-12 or Jan-Dec): ").strip().lower()

    # If the input is a number check it is between 1 and 12
    if input_month.isdigit():
        month_num = int(input_month)
        if 1 <= month_num <= 12:
            print(f"Valid input: Month number {month_num}")
            return month_num
        else:
            print("Please enter a number between 1 and 12.")
                
    # Try matching to 3-letter month
    elif input_month[:3] in month_lookup:
        month_num = month_lookup[input_month[:3]]
        print(f"Valid input: Month number {month_num}")
        return month_num
        
    else:
        print("Invalid input. Please enter a number (1–12) or the first three letters of a month (e.g., Jan, Feb, Mar).")
        
def get_actor_by_month(month_num):
    print(f"Fetching actors born in month: {month_num}")
    # Connect to MySQL
    try: 
        con = msql.connect(host='localhost', database='appdbproj', user='root', password='') 
        
        # Select the database
        cursor = con.cursor()
    
        # Command to select the data from the table
        sql = """
        SELECT ActorName, ActorDOB, ActorGender
        FROM actor
        WHERE MONTH(ActorDOB) = %s
        """
        month_num = int(month_num)  # Ensure month_num is an integer
        #  Execute the command
        cursor.execute(sql, (month_num,))

        # Fetch the results
        results = cursor.fetchall()

        if results:
            print(f"Details for Actors Born in {month_num}:")
            for name, dob, gender in results:
                # Format the date to YYYY-MM-DD
                formatted_dob = dob.strftime('%Y-%m-%d')
                print(f"{name} {formatted_dob} {gender}")
        else:
            print(f"No results found for actors born in {month_num}.")
            
    except msql.Error as err:
        print(f"Error: {err}")
    
    finally:
        cursor.close()
        con.close()
        