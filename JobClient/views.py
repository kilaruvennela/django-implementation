from jobclient import app
import json
import requests
from flask import (redirect, render_template, request, url_for)
import uuid


@app.route('/',methods=['GET'])
def index():
    #return redirect(url_for('home'))
    return render_template('home.jinja2')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.jinja2')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.jinja2')

@app.route('/is-google-login', methods=['GET'])
def is_google():
    return render_template('google-login.jinja2')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template('dashboard.jinja2')

@app.route('/signup', methods=['GET'])
def signup():
    return render_template('signup.jinja2')

@app.route('/redirect', methods=['GET'])
def redirect():
    return render_template('redirect.jinja2')