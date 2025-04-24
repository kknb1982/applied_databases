import sql_appdbproj
import neo4j_functions


from datetime import datetime
studio_cache = None

def get_birth_month(input_month):
	month_lookup = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

# If the input is a number check it is between 1 and 12
	while True:
		if input_month.isdigit():
			month_num = int(input_month)
			if 1 <= month_num <= 12:
				print(f"Valid input: Month number {month_num}")
				return month_num
			else:
				print("Enter month: ")
			
		elif input_month[:3] in month_lookup:
			month_num = month_lookup[input_month[:3]]
			return month_num
		else:
			print("Enter month: ")
		

# Create the options menu
def menu():
	while True:
		try:
			options = "\nMENU \n====\n 1 - View Directors & Film \n 2 - View Actors by Month of Birth \n 3 - Add New Actor \n 4 - View Married Actors \n 5 - Add Actor Marriage \n 6 - View Studios \n x - Exit Application"
			print(options)

			choice = input("Choice: ")

			if choice == "1":
				director_name = input("Enter director name: ")
				directors = sql_appdbproj.get_directors_by_name(director_name)
				print(f"Details for Director: {director_name} \n ------------")
				if not directors:
					print("No directors found of that name.")
					continue
				else:
					print("--------------------------------")
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
						break
					else:
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
				actor = neo4j_functions.check_actor_exists(int(actor_id))
				if not actor:
					print(f"Error: Actor ID {actor_id} does not exist.")
					continue
				else:
					married = neo4j_functions.find_spouse(actor_id)
					if married:
						print("\n ----------------------\nThese actors are married:")
						for spouse in married:
							print(f"Actor {actor_id} is married to Actor {spouse['SpouseID']}")
					else:
						print("This actor is not married. No spouse found.")
				
			elif choice == "5":
				while True:
				# Prompt for Actor 1 ID
					actor_id = input("Enter Actor 1 ID: ")
					actor1 = neo4j_functions.check_actor_exists(actor_id)
					if actor1 is None:
						print(f"Error: Actor ID {actor_id} does not exist. Please try again.")
						continue  # Re-prompt for valid Actor 1 ID

				# Prompt for Actor 2 ID
					actor2_id = input("Enter Actor 2 ID: ")
					actor2 = neo4j_functions.check_actor_exists(actor2_id)
					if actor2 is None:
						print(f"Error: Actor ID {actor2_id} does not exist. Please try again.")
						continue  # Re-prompt for valid Actor 2 ID

				# If both IDs are valid, break out of the loop
					break

    # Check if either actor is already married and not divorced
				married1 = neo4j_functions.is_actor_married(actor_id)
				married2 = neo4j_functions.is_actor_married(actor2_id)
				divorced1 = neo4j_functions.was_divorced(actor_id)
				divorced2 = neo4j_functions.was_divorced(actor2_id)

				errors = []

				if married1 and not divorced1:
					errors.append(f"Actor {actor_id} is already married and hasn't been divorced.")
				if married2 and not divorced2:
					errors.append(f"Actor {actor2_id} is already married and hasn't been divorced.")
				if errors:
					for error in errors:
						print(error)
				else:
					if neo4j_functions.create_marriage(actor_id, actor2_id):
						print(f"Marriage created between Actor {actor_id} and Actor {actor2_id}.")
					else:
						print(f"Error: Could not create marriage between Actor {actor_id} and Actor {actor2_id}.")
				
			elif choice == "6":
				global studio_cache
				# Check if the cache is empty
				if studio_cache is None:
					print("Fetching studio data from the database...")
					studio_cache = sql_appdbproj.get_studios()
				else:
					print("Using cached studio data.")
				for studio in studio_cache:
						print(f"{studio['StudioID']} | {studio['StudioName']}")

			elif choice == "x":
				print("Exiting application...")
				try:
					sql_appdbproj.close_connection()
				except Exception as e:
					print(f"(Optional) Could not close SQL connection: {e}")
				try:
					neo4j_functions.driver.close()
				except Exception as e:
					print(f"(Optional) Could not close Neo4j driver: {e}")

				break

			else:
				print(f"Invalid choice. Please try again.")

		except Exception as e:
			print(f"An error occurred: {e}")
