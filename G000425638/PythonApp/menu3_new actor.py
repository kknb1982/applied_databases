# Fuction to add a new actor
def add_new_actor(id, name, dob, gender, country_id):
    try:
        # Establish a connection to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="your_database"
        )

        cursor = connection.cursor()

        # SQL query to insert a new actor
        query = """
        INSERT INTO actors (id, name, dob, gender, country_id)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (id, name, dob, gender, country_id)

        # Execute the query
        cursor.execute(query, values)

        # Commit the transaction
        connection.commit()

        print("Actor added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # Close the database connection
        if connection.is_connected():
            cursor.close()
            connection.close()