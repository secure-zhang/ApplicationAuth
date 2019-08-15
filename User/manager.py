# -*- conding = utf-8 -*-

from __init__ import app
from flask import render_template,redirect,url_for
from gevent.pywsgi import WSGIServer

@app.route('/',methods=['GET','POST'])
def test():
    return redirect(url_for('index'))

# 异常处理
@app.errorhandler(400)
def not_found(e):
    return render_template('test.html')

if __name__ == '__main__':
    # http_server = WSGIServer(('127.0.0.1', 8080), app)
    # http_server.serve_forever()
    app.run('127.0.0.1', 8080)