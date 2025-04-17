from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "neo4jneo4j"
driver = GraphDatabase.driver(uri, auth=(username, password))

def check_actor_exists(actor_id):
    result = session.execute_read(lambda tx: tx.run("MATCH (a:Actor {ActorID: $id}) RETURN a", id=actor_id).single())
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

def create_marriage(tx, actor1id, actor2id):
    with driver.session() as session:
        session.execute_write(lambda tx: tx.run(
            """
            MATCH (a:Actor {ActorID: $id1}), (b:Actor {ActorID: $id2})
            CREATE (a)-[:MARRIED_TO]->(b)
            """, id1=actor1id, id2=actor2id))
    print(f"Actor {actor1id} is now married to Actor {actor2id}.")    

actor1id = input("Enter Actor 1 ID: ")
actor2id = input("Enter Actor 2 ID: ")

create_marriage(actor1id, actor2id)
driver.close()