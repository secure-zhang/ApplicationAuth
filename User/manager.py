# -*- conding = utf-8 -*-

from __init__ import app
from flask import render_template,redirect,url_for
from gevent.pywsgi import WSGIServer

@app.route('/',methods=['GET','POST'])
def test():
    return redirect(url_for('index'))
@app.route('/image',methods=['GET','POST'])
def image():
    return render_template('user/image_flask.html')
# 异常处理
@app.errorhandler(429)
@app.errorhandler(404)
def not_found(e):
    return render_template('test.html')


if __name__ == '__main__':
    # http_server = WSGIServer(('0.0.0.0', 8080), app)
    # http_server.serve_forever()
    app.run('127.0.0.1', 8080)