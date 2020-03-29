# app/profile/views.py

from flask import render_template
from flask_login import login_required

from . import profile


@profile.route('/make-profile')
def make_profile():
    """
    Render the page to make a profile
    """
    return render_template('profile/make_profile.html', title="Make a Profile")


@profile.route('/profile')
@login_required
def profile():
    """
    Render the user's profile
    """
    return render_template('profile/profile.html', title="My Profile")