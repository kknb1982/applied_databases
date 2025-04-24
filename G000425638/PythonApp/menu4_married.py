from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "neo4jneo4j"
driver = GraphDatabase.driver(uri, auth=(username, password))

def find_spouse(actor_id):
    with driver.session() as session:
        result = session.execute_read(lambda tx: tx.run(
            """
            MATCH (a:Actor {ActorID: $id})-[:MARRIED_TO]-(spouse:Actor)
            RETURN spouse.ActorID AS SpouseID, spouse.ActorName AS SpouseName
            """, id=actor_id).data())
        return result  # Returns a list of spouses

