# app/post/views.py

from flask import render_template
from flask_login import login_required

from . import post
from .forms import FilterForm
from .. import db
from ..models import Post

@post.route('/')
@login_required
def list_post():
    """
    List all posts which statisfy the conditions
    """
    return render_template


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