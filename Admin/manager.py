# -*- conding = utf-8 -*-

from __init__ import app
from flask import render_template,redirect,url_for
from gevent.pywsgi import WSGIServer

@app.route('/',methods=['GET'])
def test():
    return redirect(url_for('adminLogin'))

# 异常处理
@app.errorhandler(400)
@app.errorhandler(404)
def not_found(e):
    return render_template('test.html')

if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 8081), app)
    http_server.serve_forever()
    # app.run('127.0.0.1', 8081)