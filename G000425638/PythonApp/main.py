from menu1_directors import get_directors_by_name

options = "MENU \n 1 - View Directors & Film \n 2 - View Actors by Month of Birth \n 3 - Add New Actor \n 4 - View Married Actors \n 5 - Add Actor Marriage \n 6. View Studios \n x - Exit Application"
print(options)

choice = input("Choose a menu option: ")

if choice == "1":
    get_directors_by_name()
