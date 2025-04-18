from neo4j import GraphDatabase

uri = "neo4j://localhost:7687"
username = "neo4j"
password = "neo4jneo4j"
driver = GraphDatabase.driver(uri, auth=(username, password))

def check_marriage(actor_id):
    driver = GraphDatabase.driver(uri, auth=(username, password))
    with driver.session() as session:
        result = session.execute_read(find_marriage, actor_id)

        if result:
            print("These actors are married:")
            for pair in result:
                print(f"Actor ID: {pair['id1']} - Name: {pair['name1']}")
                print(f"Actor ID: {pair['id2']} - Name: {pair['name2']}")
        else:
            print("No marriage found for that actor ID.")

    driver.close()

def find_marriage(tx, actor_id):
    query = """
    MATCH (a:Actor {ActorID: $actor_id})-[r:MARRIED_TO]-(partner:Actor)
    RETURN a.ActorID AS id1, a.name AS name1,
           partner.ActorID AS id2, partner.name AS name2
    """
    return list(tx.run(query, actor_id=int(actor_id)))

