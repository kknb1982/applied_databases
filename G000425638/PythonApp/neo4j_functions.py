from neo4j import GraphDatabase
import subprocess
import time

def start_neo4j():
    try:
        print("Starting Neo4j database...")
        subprocess.run([r"C:\Users\appDB\Documents\neo4j-community-5.15.0-windows\neo4j-community-5.15.0\bin\neo4j.bat", "start"], check=True)
        print("Neo4j database started successfully.")
        time.sleep(10)  # Wait for a few seconds to ensure Neo4j is up
    except subprocess.CalledProcessError as e:
        print(f"Error starting Neo4j: {e}")
        raise

start_neo4j()
    
uri = "bolt://localhost:7687"
username = "neo4j"
password = "neo4jneo4j"
driver = GraphDatabase.driver(uri, auth=(username, password))

# Specify the database name
database_name = "actorsMarried"

def check_actor_exists(actor_id):
    with driver.session(database=database_name) as session:
        result = session.execute_read(lambda tx: tx.run(
            "MATCH (a:Actor {ActorID: $id}) RETURN a", id=actor_id).single())
        return result is not None
    
def is_actor_married(actor_id):
    with driver.session(database=database_name) as session:
        result = session.execute_read(lambda tx: tx.run(
            """
            MATCH (a:Actor {ActorID: $id})-[:MARRIED_TO]-(:Actor)
            RETURN a
            """, id=actor_id).single())
        return result is not None

def was_divorced(actor_id):
    with driver.session(database=database_name) as session:
        result = session.execute_read(lambda tx: tx.run(
            """
            MATCH (a:Actor {ActorID: $id})-[:DIVORCED_FROM]-(b:Actor)
            RETURN a
            """, id=actor_id).single())
        return result is not None
    
def get_valid_actor(prompt_text):
    while True:
        try:
            actor_id = int(input(prompt_text))
            if check_actor_exists(actor_id):
                return actor_id
            else:
                print(f"Actor with ID {actor_id} does not exist. Try again.")
        except ValueError:
            print("Please enter a valid numeric ID.")

def create_marriage(actor1id, actor2id):
    actor1id = int(actor1id)
    actor2id = int(actor2id)
    with driver.session(database=database_name) as session:
        session.execute_write(lambda tx: tx.run(
            """
            MERGE (a:Actor {ActorID: $id1})
            MERGE (b:Actor {ActorID: $id2})
            MERGE (a)-[:MARRIED_TO]->(b)
            """, id1=actor1id, id2=actor2id))
    return True

def find_spouse(actor_id):
    with driver.session(database=database_name) as session:
        result = session.execute_read(lambda tx: tx.run(
            """
            MATCH (a:Actor {ActorID: $id})-[:MARRIED_TO]-(spouse:Actor)
            RETURN spouse.ActorID AS SpouseID
            """, id=actor_id).data())
        return result
    
def driver_close():
    if driver:
        driver.close()