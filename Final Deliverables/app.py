# -*- coding: utf-8 -*-
"""
Created on Wed Nov 16 15:59:12 2022

@author: admin
"""

from flask import Flask, render_template, request, redirect, url_for, session
import ibm_db
import re
app = Flask(__name__)
app.secret_key = 'a'
conn = ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=ksm24043;PWD=ZXsdfH0rppztWofo",'','')
@app.route('/')
def home():
return render_template('register.html')
@app.route('/login', methods =['GET', 'POST'])
def login():
global userid
msg = ''
if request.method == 'POST'and 'username' in request.form and 'password' in request.form:
username = request.form['username']
password = request.form['password']
stmt = ibm_db.prepare(conn,'SELECT * FROM accounts WHERE username = ?AND password = ?')
ibm_db.bind_param(stmt,1,username)
ibm_db.bind_param(stmt,2,password)
ibm_db.execute(stmt)
account = ibm_db.fetch_assoc(stmt)
if account:
session['loggedin'] = True
session['username'] = account['USERNAME']
msg = 'Logged in successfully !'
return render_template('index.html', msg = msg)
else:
msg = 'Incorrect username / password !'
return render_template('login.html', msg = msg)
@app.route('/logout')
def logout():
session.pop('loggedin', None)
session.pop('id', None)
session.pop('username', None)
return redirect(url_for('login'))
@app.route('/register', methods =['GET', 'POST'])
def register():
msg = ''
if request.method == 'POST':
username = request.form['username']
email = request.form['email']
password = request.form['password']
sql = "SELECT * FROM accounts WHERE username = ? "
stmt = ibm_db.prepare(conn,sql)
ibm_db.bind_param(stmt,1,username)
ibm_db.execute(stmt)
account = ibm_db.fetch_assoc(stmt)
print(account)
if account:
msg = 'Account already exists !'
elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
msg = 'Invalid email address !'
elif not re.match(r'[A-Za-z0-9]+', username):
msg = 'Username must contain only characters and numbers !'
elif not username or not password or not email:
msg = 'Please fill out the form !'
else:
insert_sql = "INSERT INTO accounts VALUES (?, ?, ?)"
stmt = ibm_db.prepare(conn,insert_sql)
ibm_db.bind_param(stmt, 1, username)
ibm_db.bind_param(stmt, 2, email)
ibm_db.bind_param(stmt, 3, password)
ibm_db.execute(stmt)
msg = 'You have successfully registered !'
elifrequest.method == 'POST':
msg = 'Please fill out the form !'
return render_template('register.html', msg = msg)
if __name__ == '__main__':
app.run(debug = True)