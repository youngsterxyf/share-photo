#!/usr/bin/env python

from flask import Flask
from flask import request, redirect, url_for
from flask import render_template
from flask.ext.basicauth import BasicAuth
from utils import generate_name, generate_small_version
from db import Redis
import json

app = Flask(__name__)
app.config['db'] = Redis()

app.config['BASIC_AUTH_USERNAME'] = 'xiayf'
app.config['BASIC_AUTH_PASSWORD'] = 'abc123'

basic_auth = BasicAuth(app)

@app.route('/')
@basic_auth.required
def index():
    return render_template('index.html', photos=app.config['db'].get_all())

@app.route('/upload', methods=['POST'])
def upload():
    for _, f in request.files.iteritems():
        suffix = f.filename.split('.')[-1]
        target_name = '{0}.{1}'.format(generate_name(), suffix)
        image_path = 'static/uploads/' + target_name
        f.save(image_path)
        small_image_path = generate_small_version(image_path)
        app.config['db'].set(image_path, small_image_path)
    return json.dumps({'success': True})


if __name__ == '__main__':
    app.run(debug=True)