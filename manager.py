# -*- conding = utf-8 -*-

from __init__ import app
from flask import render_template

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login',methods=['GET','POST'])
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run('192.168.1.3',5000)