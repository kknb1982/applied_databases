from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "neo4jneo4j"
driver = GraphDatabase.driver(uri, auth=(username, password))

def find_spouse(actor_id):
    query = """
    MATCH (a:Actor {ActorID: $actorId})-[:MARRIED_TO]-(spouse:Actor)
    RETURN a.ActorID AS ActorID, a.ActorName AS ActorName, spouse.ActorID AS SpouseID, spouse.ActorName AS SpouseName
    """
    with driver.session() as session:
        result = session.run(query, actorId=int(actor_id))
        return list(result)

