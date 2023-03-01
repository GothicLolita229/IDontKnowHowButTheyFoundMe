# -*- coding: utf-8 -*-
"""
Created on Sat Feb  4 15:27:43 2023

@author: vianacbutler
"""

from flask import Flask, request, render_template, redirect, url_for
import pickle

# app = Flask(__name__)

 # The database to store username and password
 #users = {'username': 'password'}

# @app.route('/')
# def index():
#     return render_template('login.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username in users and users[username] == password:
#             return redirect(url_for('secret'))
#         else:
#             return 'Invalid username/password combination'
#     return render_template('login.html')

# @app.route('/secret')
# def secret():
#     return 'You have logged in successfully!'



# if __name__ == '__main__':
#     app.run(debug=True)


app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            return redirect(url_for('secret'))
        else:
            return 'Invalid username/password combination'
    return render_template('login.html')

@app.route('/secret')
def secret():
    return 'You have logged in successfully!'

def add_user(username, password):
    with open('users.pkl', 'ab') as f:
        pickle.dump({username: password}, f)

def check_user(username, password):
    with open('users.pkl', 'rb') as f:
        while True:
            try:
                user = pickle.load(f)
                if username in user and user[username] == password:
                    return True
            except EOFError:
                break
    return False

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_user(username, password):
            return 'User already exists'
        add_user(username, password)
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
