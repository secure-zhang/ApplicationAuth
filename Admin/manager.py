# -*- conding = utf-8 -*-

from __init__ import app
from flask import render_template

@app.route('/',methods=['GET'])
def test():
    return render_template('test.html')

# 异常处理
@app.errorhandler(400)
def not_found(e):
    return render_template('test.html')

if __name__ == '__main__':
    app.run('192.168.1.7',5000)