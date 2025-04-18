import sql_appdbproj
import menu4_married
import menu5_add_marriage


from datetime import datetime
studio_cache = None

def get_birth_month(input_month):
	month_lookup = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}

# If the input is a number check it is between 1 and 12
	if input_month.isdigit():
		month_num = int(input_month)
		if 1 <= month_num <= 12:
			print(f"Valid input: Month number {month_num}")
			return month_num
		else:
			print("Invalid input. Please enter a number (1–12) or the first three letters of a month (e.g., Jan, Feb, Mar).")
			return None
	elif input_month[:3] in month_lookup:
		month_num = month_lookup[input_month[:3]]
		print(f"Valid input: Month number {month_num}")
		return month_num
	else:
		print("Invalid input. Please enter a number (1–12) or the first three letters of a month (e.g., Jan, Feb, Mar).")
		return None

# Create the options menu
def menu():
	while True:
		try:
			options = "MENU \n 1 - View Directors & Film \n 2 - View Actors by Month of Birth \n 3 - Add New Actor \n 4 - View Married Actors \n 5 - Add Actor Marriage \n 6 - View Studios \n x - Exit Application"
			print(options)

			choice = input("Choose a menu option: ")

			if choice == "1":
				director_name = input("Enter the name of a director or part thereof: ")
				directors = sql_appdbproj.get_directors_by_name(director_name)
				for director in directors:
					print(director["DirectorName"], "|", director["FilmName"], "|", director["StudioName"])
					break
				else:
					print(f"No results found for '{director_name}'.")

			elif choice == "2":
				input_month = input("Enter the month of birth you are interested in (1-12 or Jan-Dec): ").strip().lower()
				month_num = get_birth_month(input_month)
				if month_num:
					results_actor = sql_appdbproj.get_actor_by_month(month_num)
					print(f"Details for Actors Born in {month_num}:")
					for actor in results_actor:
						dob = actor["ActorDOB"]
						# Format the date to DD-MM-YYYY
						formatted_dob = datetime.strptime(dob, '%Y-%m-%d').strftime('%d-%m-%Y')
						print(actor["Name"], "|", formatted_dob, "|", actor["gender"])
						break
					else:
						print(f"No results found for actors born in {month_num}.")	

			elif choice == "3":
				actor_id = input("Enter Actor ID: ")
				actor = sql_appdbproj.check_actor(actor_id)
				if actor is not None:
					print(f"Error: Actor ID {actor_id} already exists.")
				else:
					name = input("Enter Actor Name: ")
					dob = input("Enter Actor Date of Birth (YYYY-MM-DD): ")
					
					# Validate date format
					try:
						datetime.strptime(dob, '%Y-%m-%d')
					except ValueError:
						print("Incorrect date format, should be YYYY-MM-DD")
						dob = input("Enter Actor Date of Birth (YYYY-MM-DD): ")

					gender = input("Enter Actor Gender: ").strip()
					while gender not in ['Male', 'Female', 'M', 'F']:
						print("Invalid gender. Please enter 'M', 'F', 'Male', or 'Female'.")
						gender = input("Enter Actor Gender (M/F): ")
						gender = "Male" if gender in ['M', 'Male'] else "Female"
					
					country_id = input("Enter Country ID: ")
					sql_appdbproj.check_country(country_id)
					while True:
						sql_appdbproj.add_actor(actor_id, name, dob, gender, country_id)
						new_actor = sql_appdbproj.show_added_actor(actor_id)
						if new_actor:
							print("Actor successfully added")
							print(f"Actor ID: {new_actor['ActorID']}")
							print(f"Actor Name: {new_actor['ActorName']}")
							print(f"Actor DOB: {new_actor['ActorDOB']}")
							print(f"Actor gender: {new_actor['ActorGender']}")
							print(f"Actor Country ID: {new_actor['ActorCountryID']}")

						else:
							print(f"Error: Actor ID {actor_id} not found in the database.")
						break
			
			elif choice == "4":
				actor_id = input("Enter the Actor ID to check for marriages: ")
				actor = menu5_add_marriage.check_actor_exists(int(actor_id))
				if actor is None:
					print(f"Error: Actor ID {actor_id} does not exist.")
					break
				else:
					married = menu4_married.find_spouse(actor_id)
					if married:
						print("These actors are married:")
						for record in married:
							print(f"{record["ActorID"]} | {record["ActorName"]}")
							print(f"{record['SpouseID']} | {record['SpouseName']}")
							break
						else:
							print(f"Actor {actor_id} is not married.")
					break
				
			
			elif choice == "5":
				actor_id = input("Enter the Actor ID to check for marriages: ")
				actor1 = menu4_married.actor_exists(actor_id)
				if actor1 is None:
					print(f"Error: Actor ID {actor1} does not exist.")
					break
				else:
					actor2_id = input("Enter the second Actor ID to check for marriages: ")
					actor2 = menu4_married.actor_exists(actor2_id)
					if actor2 is None:
						print(f"Error: Actor ID {actor2_id} does not exist.")
						break
					else:
						married1 = menu4_married.is_actor_married(actor_id)
						married2 = menu4_married.is_actor_married(actor2_id)
						divorced1 = menu4_married.has_been_divorced(actor_id)
						divorced2 = menu4_married.has_been_divorced(actor2_id)
						errors = []
						if married1 and not divorced1:
							errors.append(f"Actor {actor_id} is already married and hasn't been divorced.")
						if married2 and not divorced2:
							errors.append(f"Actor {actor2_id} is already married and hasn't been divorced.")
						if errors:
							for error in errors:	
								print(error)
						else:
							create_marriage = menu4_married.create_marriage(actor_id, actor2_id)
							if create_marriage:
								print(f"Marriage created between Actor {actor_id} and Actor {actor2_id}.")
							else:
								print(f"Error: Could not create marriage between Actor {actor_id} and Actor {actor2_id}.")
							break
				
			elif choice == "6":
				global studio_cache
				# Check if the cache is empty
				if studio_cache is None:
					print("Fetching studio data from the database...")
					studio_cache = sql_appdbproj.get_studios()
				else:
					print("Using cached studio data.")
				for studio in studio_cache:
						print(studio)

			elif choice == "x":
				print("Exiting application...")
				try:
					sql_appdbproj.close_connection()
				except Exception as e:
					print(f"(Optional) Could not close SQL connection: {e}")
				try:
					menu5_add_marriage.driver.close()
				except Exception as e:
					print(f"(Optional) Could not close Neo4j driver: {e}")

				break

			else:
				print(f"Invalid choice. Please try again.")

		except Exception as e:
			print(f"An error occurred: {e}")
