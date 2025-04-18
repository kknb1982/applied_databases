import pymysql

con = None

def connect():
	global con
	con = pymysql.connect(host='localhost', database='appdbproj', user='root', password='', cursorclass=pymysql.cursors.DictCursor) 

# Get directors by name function
def get_directors_by_name(director_name):
	if (not con):
			connect();

# Command to select the data from the table
	sql = "SELECT d.DirectorName, f.FilmName, s.StudioName FROM director d JOIN film f ON d.DirectorID = f.FilmDirectorID JOIN studio s ON f.FilmStudioID = s.StudioID WHERE d.DirectorName LIKE %s"

#  Execute the command
	with con:
		cursor = con.cursor()
		cursor.execute(sql, ('%' + director_name + '%',))
# Fetch the results
		director_results = cursor.fetchall()
		return director_results




def get_actor_by_month(month_num):
# Connect to SQL
	if (not con):
		connect();    
# Command to select the data from the table
	sql = "SELECT ActorName, ActorDOB, ActorGender FROM actor WHERE MONTH(ActorDOB) = %s"
	month_num = int(month_num) 

#  Execute the command
	with con:
		cursor = con.cursor()
		cursor.execute(sql, (month_num,))
		results_actor = cursor.fetchall()
		return results_actor



def check_actor(actor_id):
# Connect to SQL
	if (not con):
		connect();    
# Check if actor ID already exists
	sql = "SELECT * FROM actor WHERE ActorID = %s"
	value = (actor_id,)  
        
#  Execute the command
	with con:
		cursor = con.cursor()
		cursor.execute(sql, value)
		results_actor = cursor.fetchall()
		return results_actor


def check_country(country_id):
# Connect to SQL
	if (not con):
		connect();    

	sql = "SELECT * FROM country WHERE CountryID = %s"
	value = (country_id,)

#  Execute the command
	with con:
		cursor = con.cursor()
		cursor.execute(sql, value)
		results_country = cursor.fetchone()
		return results_country
		
		if not cursor.fetchone():
			print(f"Error: Country ID {country_id} does not exist.")
			country_id = input("Enter Country ID: ")


def add_actor(actor_id, name, dob, gender, country_id):
# Connect to SQL
	if (not con):
		connect();    
# Add actor
	sql = "INSERT INTO Actor (ActorID, ActorName, ActorDOB, ActorGender, ActorCountryID) VALUES (%s, %s, %s, %s, %s)"
	values = (actor_id, name, dob, gender, country_id)

#  Execute the command
	with con:
		cursor = con.cursor()
		cursor.execute(sql, values)
		con.commit()
		print("Actor added successfully!")
            
def show_added_actor(actor_id):
# Connect to SQL
	if (not con):
		connect();
	## Retrieve the new actor's ID from the database
	sql = "SELECT * FROM actor WHERE ActorID = %s"
	value = (actor_id,)  
		
	with con:
		cursor	= con.cursor()
		cursor.execute(sql, value)
		new_actor = cursor.fetchone()
		return new_actor
            
def get_studios():
	if (not con):
		connect();
	# Command to select the data from the table
	sql = "SELECT StudioID, StudioName FROM studio ORDER BY StudioID ASC"
		
	with con:
		cursor	= con.cursor()
		cursor.execute(sql)
		studio_cache = cursor.fetchall()
		return studio_cache

def close_connection():
	if con:
		con.close()
		con = None