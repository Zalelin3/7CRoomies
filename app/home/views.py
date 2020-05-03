# app/home/views.py

from flask import Flask, render_template, request
from flask_login import login_required

from . import home

from .. import db
from ..models import Post, On_campus, User

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")


@home.route('/dashboard')
@login_required
def dashboard():
    """
    Render the dashboard template on the /dashboard route
    """
    return render_template('home/dashboard.html', title="Dashboard")

