import mysql.connector
from mysql.connector import Error 
import pandas as pd
import requests
from ast import literal_eval as make_tuple

create_login_table = ""
insert_to_login = ""

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
        print(f"Error in MySQL Connection: '{err}'")

    return connection

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error in Database Creation: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error in Database Connection: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error in Query Execution: '{err}'")

def create_login_table():
    create_login_tables = """
    CREATE TABLE login (
    email VARCHAR(255) PRIMARY KEY,
    password VARCHAR(255) NOT NULL
    );
    """
    return create_login_tables

def insert_to_login(x_text : str) -> str:
    insert_to_logins = 'INSERT INTO login VALUES ("' + x_text[0] + '",  "' + x_text[1] + '");'
    return insert_to_logins

def retrieve_from_backend(databaseURL, databaseRootUsername, databasePassword, databaseName):
    while(True):
        url = "http://localhost:5000/is_empty"
        x = requests.post(url)
        if x.text == "True":
            print("Empty?", True)
        else:
            print("Empty?", False)
            print("Popping...")
            url = "http://localhost:5000/pop"
            x = requests.post(url)
            print("Popped", make_tuple(x.text))
            connection = create_db_connection(databaseURL, databaseRootUsername, databasePassword, databaseName)
            query = insert_to_login(make_tuple(x.text))
            execute_query(connection, query)

def main(databaseURL, databaseRootUsername, databasePassword, databaseName):
    global create_login_table

    # create connection to mysql server
    connection = create_server_connection(databaseURL, databaseRootUsername, databasePassword)
    
    # create database
    create_database_query = "CREATE DATABASE " + databaseName
    create_database(connection, create_database_query)

    # query for table creation
    create_login_table = create_login_table()

    # create the table we will store data into.
    connection = create_db_connection(databaseURL, databaseRootUsername, databasePassword, databaseName) # Connect to the Database
    execute_query(connection, create_login_table) # Execute our defined query

    # add stuff to the table from our connection to backend.py
    retrieve_from_backend(databaseURL, databaseRootUsername, databasePassword, databaseName)

# change parameters accordingly for your specific MySQL database
if __name__ == "__main__":
    databaseURL = "localhost"
    databaseRootUsername = "root"
    databasePassword = "root"
    databaseName = "form_results"
    main(databaseURL, databaseRootUsername, databasePassword, databaseName)