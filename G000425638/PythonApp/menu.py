# Project: MoviesDB
# Created: April 2025
# Author: Kirstin Barnett
# Description: This is the menu file for the MoviesDB application. It creates the menu and handles user input.

# Import necessary modules
import sql_appdbproj
import neo4j_functions
from datetime import datetime

studio_cache = None  # Initialize studio_cache to None

# Function to get the birth month from user input. It accepts both numeric and string formats (e.g., "1", "jan", "February"). It validates the input and returns the corresponding month number (1-12). If the input is invalid, it prompts the user to enter a valid month until a correct input is provided.
def get_birth_month(input_month):
	month_lookup = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

	# If the input is a number, check it is between 1 and 12
	while True:
		if input_month.isdigit():
			month_num = int(input_month)
			if 1 <= month_num <= 12:
				print(f"Valid input: Month number {month_num}")
				return month_num
			else:
				print("Enter month: ")
		
		# If the input is a string, check if it is in the month_lookup dictionary
		elif input_month[:3] in month_lookup:
			month_num = month_lookup[input_month[:3]]
			return month_num
		else:
			print("Enter month: ")
		

# Options menu for the MoviesDB application. It provides a list of options for the user to choose from. Each option corresponds to a specific function in the application, such as viewing directors and films, adding new actors, viewing married actors, etc. The menu continues to display until the user chooses to exit the application.
# The menu also handles user input and validates it. If the input is invalid, it prompts the user to enter a valid choice. It also handles exceptions that may occur during the execution of the menu options.
def menu():
    global studio_cache
    
    while True:
        try:
			# Diplay the menu options to the user and prompt for a choice
			options = "\nMENU \n====\n1 - View Directors & Film\n2 - View Actors by Month of Birth\n3 - Add New Actor\n4 - View Married Actors\n5 - Add Actor Marriage\n6 - View Studios\n7 - Add Studio\nx - Exit Application"
			print(options)

			choice = input("Choice: ")
		except Exception as e:
			print(f"An error occurred: {e}")

		if choice == "1":
			director_name = input("Enter director name: ")
			directors = sql_appdbproj.get_directors_by_name(director_name)
			print(f"Details for Director: {director_name} \n --------")
			if not directors:
				print("No directors found of that name.")
				continue
			else:
				print("------------------")
				for director in directors:
					print(director["DirectorName"], "|", director["FilmName"], "|", director["StudioName"])
					break
		elif choice == "2":
			input_month = input("Enter month: ").strip().lower()
			month_num = get_birth_month(input_month)
			if month_num:
				results_actor = sql_appdbproj.get_actor_by_month(month_num)
				print(f"Details for Actors Born in {input_month}:")
				for actor in results_actor:
					dob = actor["ActorDOB"]
					if isinstance(dob, str):
						dob = datetime.strptime(dob, '%Y-%m-%d')  # Convert string to datetime
					formatted_dob = dob.strftime('%d-%m-%Y')  # Format the date						dob = actor["ActorDOB"]
					print(actor["ActorName"], "|", formatted_dob, "|", actor["ActorGender"])
				else:
					if not results_actor:
						print(f"No results found for actors born in {month_num}.")	

		elif choice == "3":
			print("Add New Actor\n-----------------\n ")
			actor_id = input("Enter Actor ID: ")
			actor = sql_appdbproj.check_actor(actor_id)
			if actor is not None:
				print(f"*** ERROR ****: Actor ID {actor_id} already exists.")
			else:
				name = input("Enter Actor Name: ")
				dob = input("Enter Actor Date of Birth (YYYY-MM-DD): ")
					
				# Validate date format
				while True:
					try:
						dob = datetime.strptime(dob, '%Y-%m-%d')
						break  # Exit the loop if the date is valid
					except ValueError:
						print("Incorrect date format, should be YYYY-MM-DD")
						dob = input("Enter Actor Date of Birth (YYYY-MM-DD): ")

				gender = input("Enter Actor Gender: ").strip()
				while gender not in ['Male', 'Female', 'M', 'F']:
					print("Invalid gender. Please enter 'M', 'F', 'Male', or 'Female'.")
					gender = input("Enter Actor Gender (M/F): ")
					
				gender = "Male" if gender in ['M', 'Male'] else "Female"
					
				while True:
					country_id = input("Enter Country ID: ")
					country = sql_appdbproj.check_country(country_id)					
					if country is None:
						print(f"*** ERROR ***: Country ID {country_id} does not exist.")
					else:
						break

				sql_appdbproj.add_actor(actor_id, name, dob, gender, country_id)
											
				new_actor = sql_appdbproj.show_added_actor(actor_id)
				if new_actor:
					print("\nActor successfully added")
					print(f"Actor ID: {new_actor['ActorID']}", "|", )
					print(f"Actor Name: {new_actor['ActorName']}")
					print(f"Actor DOB: {new_actor['ActorDOB']}")
					print(f"Actor gender: {new_actor['ActorGender']}")
					print(f"Actor Country ID: {new_actor['ActorCountryID']}")

				else:
					print(f"Error: Actor ID {actor_id} not found in the database.")
					break
			
		elif choice == "4":
			actor_id = input("Actor ID: ")
			actor_id = int(actor_id)
			actor = neo4j_functions.check_actor_exists(actor_id)
			if not actor:
				print(f"Error: Actor ID {actor_id} does not exist.")
				continue
			else:
				married = neo4j_functions.find_spouse(actor_id)
				if married:
					print("\n ----------------------\nThese actors are married:")
					actor1 = sql_appdbproj.check_actor(actor_id)
					print(f"{actor1['ActorID']} | {actor1['ActorName']}")
					for spouse in married:
						spouse_details = sql_appdbproj.check_actor(spouse['SpouseID'])
						print(f"{spouse['SpouseID']} | {spouse_details['ActorName']}")
				else:
					print("This actor is not married. No spouse found.")
				
		elif choice == "5":
			while True:
			# Prompt for Actor 1 ID
				actor_id = input("Enter Actor 1 ID: ")
				actor_id = int(actor_id)
				actor1 = sql_appdbproj.check_actor(actor_id)
				if not actor1:
					print(f"Error: Actor ID {actor_id} does not exist. Please try again.")
					continue  # Re-prompt for valid Actor 1 ID

			# Prompt for Actor 2 ID
				actor2_id = input("Enter Actor 2 ID: ")
				actor2_id = int(actor2_id)
				actor2 = sql_appdbproj.check_actor(actor2_id)
				if not actor2:
					print(f"Error: Actor ID {actor2_id} does not exist. Please try again.")
					continue  # Re-prompt for valid Actor 2 ID

			# If both IDs are valid, break out of the loop
				break

			# Check if the two actors are already married to each other
			already_married = neo4j_functions.find_spouse(actor_id)
			if any(spouse['SpouseID'] == actor2_id for spouse in already_married):
				print(f"Error: Actor {actor_id} and Actor {actor2_id} are already married.")
			else:
			# Check if either actor is already married to someone else
				married1 = neo4j_functions.is_actor_married(actor_id)
				married2 = neo4j_functions.is_actor_married(actor2_id)
				errors = []
				if married1:
					errors.append(f"Actor {actor_id} is already married to someone else.")
				if married2:
					errors.append(f"Actor {actor2_id} is already married to someone else.")
				if errors:
					for error in errors:
						print(error)
				else:
				# Create the marriage if both actors are not married
					if neo4j_functions.create_marriage(actor_id, actor2_id):
						print(f"Marriage created between Actor {actor_id} and Actor {actor2_id}.")
					else:
						print(f"Error: Could not create marriage between Actor {actor_id} and Actor {actor2_id}.")
				
		elif choice == "6":
		# Ensure studio_cache is initialized with the full list of studios
			try:
				if studio_cache is None:
					print("Fetching studio list from the database...")
					studio_cache = sql_appdbproj.get_studios()
					print(f"DEBUG: studio_cache initialized: {studio_cache}")
				print("\nStudio List:")
				for studio in studio_cache:
					print(f"{studio['StudioID']} | {studio['StudioName']}")
			except Exception as e:
				print(f"Error fetching studio list: {e}")

		elif choice == "7":
			if studio_cache is None:
				studio_cache = sql_appdbproj.get_studios()
			
			studio_name = input("Enter the name of the studio: ")
			sql_appdbproj.add_studio_to_cache(studio_name)
			print(f"Studio '{studio_name}' added to cache.")
		
				
		elif choice == "x":
			print("Exiting application...")
			if studio_cache:
				try:
					sql_appdbproj.save_studio_cache_to_db(studio_cache)
					print("Studio cache successfully saved to the database.")
				except Exception as e:
					print(f"Error updating the studio cache: {e}")
			else:
				print("No studio cache to save.")
			# Close connections
			try:
				if sql_appdbproj.con:
					sql_appdbproj.close_connection()
			except Exception as e:
				print(f"(Optional) Could not close SQL connection: {e}")
			try:
				if neo4j_functions.driver:
					neo4j_functions.driver.close()
			except Exception as e:
				print(f"(Optional) Could not close Neo4j driver: {e}")
			break

		else:
			print(f"Invalid choice. Please try again.")

