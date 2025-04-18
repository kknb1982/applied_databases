from menu import menu
from menu1_directors import get_directors_by_name
from menu2_actor_by_dob import get_birth_month, get_actor_by_month
from menu3_new_actor import add_actor
from menu4_married import check_marriage
from menu5_add_marriage import check_actor_exists, is_actor_married, was_divorced, get_valid_actor, create_marriage
from menu6_studios import get_studios


import mysql.connector as msql
from mysql.connector import Error
from datetime import datetime
from neo4j import GraphDatabase

con = None
driver = None

  
if __name__ == "__main__":
    menu()


    
