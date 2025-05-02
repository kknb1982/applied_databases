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
	cursor = con.cursor()
	cursor.execute(sql, ('%' + director_name + '%',))
# Fetch the results
	director_results = cursor.fetchall()
	return director_results
	cursor.close()


def get_actor_by_month(month_num):
# Connect to SQL
	if (not con):
		connect();    
# Command to select the data from the table
	sql = "SELECT ActorName, ActorDOB, ActorGender FROM actor WHERE MONTH(ActorDOB) = %s"
	month_num = int(month_num) 

#  Execute the command
	cursor = con.cursor()
	cursor.execute(sql, (month_num,))
	results_actor = cursor.fetchall()
	cursor.close()	
	return results_actor




def check_actor(actor_id):
# Connect to SQL
	if (not con):
		connect();    
# Check if actor ID already exists
	sql = "SELECT * FROM actor WHERE ActorID = %s"
	value = (actor_id,)  
        
#  Execute the command
	cursor = con.cursor()
	cursor.execute(sql, value)
	results_actor = cursor.fetchone()
	cursor.close()
	return results_actor
	


def check_country(country_id):
# Connect to SQL
	if (not con):
		connect();    

	sql = "SELECT * FROM country WHERE CountryID = %s"
	value = (country_id,)

#  Execute the command
	cursor = con.cursor()
	cursor.execute(sql, value)
	results_country = cursor.fetchone()
	cursor.close()
	return results_country



def add_actor(actor_id, name, dob, gender, country_id):
# Connect to SQL
	if (not con):
		connect();    
# Add actor
	sql = "INSERT INTO Actor (ActorID, ActorName, ActorDOB, ActorGender, ActorCountryID) VALUES (%s, %s, %s, %s, %s)"
	values = (actor_id, name, dob, gender, country_id)
	print(values)
#  Execute the command
	cursor = con.cursor()
	cursor.execute(sql, values)
	con.commit()
	cursor.close()

def show_added_actor(actor_id):
# Connect to SQL
	if (not con):
		connect();
	## Retrieve the new actor's ID from the database
	sql = "SELECT * FROM actor WHERE ActorID = %s"
	value = (actor_id,)  
		

	cursor	= con.cursor()
	cursor.execute(sql, value)
	new_actor = cursor.fetchone()
	cursor.close()
	return new_actor

            
def get_studios():
	if (not con):
		connect()
	# Command to select the data from the table
	sql = "SELECT StudioID, StudioName FROM studio ORDER BY StudioID ASC"
	cursor	= con.cursor()
	cursor.execute(sql)
	studios = cursor.fetchall()
	cursor.close()
	return studios

	
def add_studio_to_cache(studio_name):
	global studio_cache
	if studio_cache is None:
		studio_cache = get_studios()
    # Create a new studio entry with a placeholder ID (e.g., None)
	new_studio = {'StudioID': None, 'StudioName': studio_name}
	studio_cache.append(new_studio)

def save_studio_cache_to_db(studio_cache):
    """Save the studio cache to the database."""
    if (not con):
        connect()
    cursor = con.cursor()
    for studio in studio_cache:
        # Only insert studios that do not have an ID (i.e., new studios)
        if studio['StudioID'] is None:
            sql = "INSERT INTO Studio (StudioName) VALUES (%s)"
            values = (studio['StudioName'],)
            cursor.execute(sql, values)
    con.commit()
    cursor.close()

def close_connection():
	global con
	if con:
		con.close()
		con = None

def get_actor_by_id(actor_id):
# Connect to SQL
	if (not con):
		connect();    
	sql = "SELECT ActorID, ActorName FROM actor WHERE ActorID = %s"
	value = (actor_id,)  
        
#  Execute the command
	cursor = con.cursor()
	cursor.execute(sql, value)
	actor_details = cursor.fetchone()
	cursor.close()
	return actor_details
