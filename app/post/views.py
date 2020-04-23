# app/post/views.py

from flask import render_template
from flask_login import login_required

from . import post


@post.route('/make-post')
@login_required
def make_post():
    """
    Render the page to make a post
    """
    return render_template('post/make_post.html', title="Make a Post")

@post.route('/make-post-offcampus')
@login_required
def make_post_offcampus():
    """
    Render the page to make a post for off-campus housing
    """
    return render_template('post/make_post_offcampus.html', title="Make a Post")

@post.route('/make-post-oncampus-suite')
@login_required
def make_post_oncampus_suite():
    """
    Render the page to make a post for on-campus suite housing
    """
    return render_template('post/make_post_oncampus_suite.html', title="Make a Post")

@post.route('/make-post-oncampus-room')
@login_required
def make_post_oncampus_room():
    """
    Render the page to make a post for on-campus room housing
    """
    return render_template('post/make_post_oncampus_room.html', title="Make a Post")