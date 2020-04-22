# app/home/views.py

from flask import Flask, render_template, request
from flask_login import login_required
import json
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

@home.route('/filter', methods=['GET', 'POST'])
@login_required
def list_oncampuspost():
    """
    List all posts which statisfy the conditions
    """
    if request.method == 'POST':
        query = """SELECT P.id, P.post_type, P.allows_pet, P.allowed_gender, P.title,
        P.description, P.capacity, P.owner_id, P.image_1, O.college, O.dorm_1,
         O.dorm_2, O.dorm_3, O.drawNo, O.nSingles, O.nDoubles,
         O.nTriples, O.nQuads 
         FROM user As U, posts As P, oncampus As O
         WHERE P.post_type = 0 AND U.id = P.owner_id AND P.id = O.post_id"""
        if request.form['school'] != "0":
            query = query + " AND O.college = "+ request.form['school']
        if request.form['pet'] != "2":
            query = query + " AND P.allows_pet = " + request.form['pet']
        # if request.form['capacity'] != "-1":
        #     query = query + "  P.capacity= " + request.form['capacity']
        # if request.form["nSingles"] != "-1":
        #     query = query + " AND O.nSingles = " + str(request.form['nSingles'])
        # if form.nDoubles != -1:
        #     query = query + " AND O.nDoubles = " + str(request.form['nDoubles'])
        # if form.nTriples != -1:
        #     query = query + " AND O.nTriples = " + str(request.form['nTriples'])
        # if form.nQuads != -1:
        #     query = query + " AND O.nQuads = " + str(request.form['nQuads'])
        # if form.partyFreq != -1:
        #     query = query + " AND U.partyFreq <= " + str(request.form['partyFreq'])
        # if form.visitorFreq != -1:
        #     query = query +" AND U.visitorFreq <= " + str(request.form['visitorFreq'])
        if request.form['wakeup'] != "0":
            query = query +" AND U.wakeup = " + request.form['wakeup']
        if request.form["bedtime"] != "0":
            query = query +" AND U.bedtime = " + request.form['bedtime']
        if request.form["noiseSen"] != "0":
            query = query +" AND U.noiseSen <= " + request.form['noiseSen']
        # if request.form["allowed_gender"] != "3":
        #     query = query + " AND P.allowed_gender = " + request.form['allowed_gender']
        posts = db.session.execute(query)
        # for post in posts:
        #     print(post["id"])
        rows = [(dict(row.items())) for row in posts]
        return render_template('home/oncamp.html', posts = rows, title = 'On Campus Filtering')
    return render_template('home/oncamp.html', posts = None, title='On Campus Filtering' )
