# app/profile/views.py

from flask import Flask, render_template, request
from flask_login import login_required

from . import profile

from .. import db
from ..models import Post, On_campus, User

@profile.route('/make-profile')
def make_profile():
    """
    Render the page to make a profile
    """
    return render_template('profile/make_profile.html', title="Make a Profile")


@profile.route('/profile', methods=["POST", "GET"])
@login_required
def profile():
    """
    Render the user's profile
    """
    if request.method == 'POST':
        postQuery = "SELECT P.id, P.post_type, P.allows_pet, P.allowed_gender, P.title,\
        P.description, P.capacity, P.owener_id, P.image_1\
            FROM user As U, posts As P\
            WHERE U.id = P.owner_id"

        # interestsQuery = "SELECT P.id, P.post_type, P.allows_pet, P.allowed_gender, P.title,\
        # P.description, P.capacity, P.owener_id, P.image_1\
        #     FROM user As U, posts As P, live As L\
        #     WHERE L.user_id = {{current_user.id}} AND L.post_id = P.id\
        #         AND L.status=___"

        # approvalsQuery = "SELECT P.id, P.post_type, P.allows_pet, P.allowed_gender, P.title,\
        # P.description, P.capacity, P.owener_id, P.image_1\
        #     FROM user As U, posts As P, live As L\
        #     WHERE L.user_id = {{current_user.id}} AND L.post_id = P.id\
        #         AND L.status=___"
    
        post = db.session.execute(postQuery)
        return render_template('profile/profile.html', post = post, title = "My Profile")

    return render_template('profile/profile.html', title="My Profile")