import mysql.connector
from mysql.connector import Error
import pandas

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection
pw="root_klap"
connection = create_server_connection("localhost", "root", pw)