# app/profile/views.py

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import profile

from .. import db
from ..models import Post, On_campus, User, Pet, Allergy, Ghost_User, Live, Off_campus

@profile.route('/make-profile', methods=["GET","POST"])
@login_required
def make_profile():
    """
    Render the page to make a profile
    """

    if request.method == 'POST':
        try:
            current_user.school = int(request.form['school'])
            current_user.gender = bool(request.form['gender'])
            current_user.is_smoke = bool(request.form['is_smoke'])
            current_user.has_car = bool(request.form['has_car'])
            current_user.has_bike = bool(request.form['has_bike'])
            current_user.noise_Sen = int(request.form['noiseSen'])
            current_user.wakeup = int(request.form['wakeup'])
            current_user.bedtime = int(request.form['bedtime'])
            current_user.partyFreq= int(request.form['partyFreq'])
            current_user.visitorFreq= int(request.form['visitorFreq'])
            db.session.commit()
            i = j = k = 0
            while 'ghostEmail'+str(i) in request.form:
                ghostEmail = request.form['ghostEmail'+str(i)]
                g_test = Ghost_User.query.filter_by(email = ghostEmail).first()
                if g_test is not None :
                    flash('This email address is used.')
                    return redirect(request.url)
                ghostFriend = Ghost_User(representer_id = current_user.id, email = ghostEmail, \
                    first_name = request.form['ghostFirstName'+str(i)],\
                    last_name = request.form['ghostLastName'+str(i)])
                db.session.add(ghostFriend)
                db.session.commit()
                i = i+1
            while 'pet'+str(j) in request.form:
                petName = request.form['pet'+str(j)]
                p_test = Pet.query.filter_by(name = petName).filter_by(user_id = current_user.id).first()
                if p_test is not None:
                    flash('You have already add this pet to your profile.')
                    return redirect(request.url)
                pet = Pet(name = petName, user_id = current_user.id)
                db.session.add(pet)
                db.session.commit()
                j = j+1
            while 'allergy'+str(k) in request.form:
                allergyName = request.form['allergy'+str(k)]
                a_test = Allergy.query.filter_by(name = allergyName).filter_by(user_id = current_user.id).first()
                if a_test is not None:
                    flash('You have already add this allergy to your profile.')
                    return redirect(request.url)
                allergy = Allergy(name = allergyName, user_id = current_user.id)
                db.session.add(allergy)
                db.session.commit()
                k = k+1
            flash('Congratulations! You have successfully build your profile. :)')
        # redirect to the dashboard page after login
            return redirect(url_for('home.dashboard'))
        except:
            flash('Error: Invalid Access !!!')
            return render_template('profile/make_profile.html', title="Make a Profile")
    return render_template('profile/make_profile.html', title="Make a Profile")


@profile.route('/ownprofile', methods=["POST", "GET"])
@login_required
def ownprofile():
    """
    Render the user's own profile
    """
    post = oncampus = offcampus = live = wait_list = ghostlive = approve = None
    post = Post.query.filter_by(owner_id=current_user.id).first()
    other_post = other_post_on= other_post_off= None
    if post is not None:
        # return all users who are interested in current user's post
        waitquery = """SELECT U.id, U.email, U.username, U.first_name, U.last_name
                    FROM user AS U, lives AS L
                    WHERE L.user_id = U.id AND L.status = 1 AND L.post_id = """ + str(post.id)
        wait_lists = db.session.execute(waitquery)
        wait_list = [(dict(k.items())) for k in wait_lists]

        if post.post_type:
            oncampus = On_campus.query.filter_by(post_id=post.id).first()
        else:
            offcampus = Off_campus.query.filter_by(post_id=post.id).first()
        
        # return all users who are lived with user
        livequery = """SELECT U.id, U.email, U.first_name, U.last_name, P.owner_id, U.username
                    FROM user AS U, lives AS L, posts AS P
                    WHERE L.user_id = U.id AND L.status = 3 AND
                    L.post_id = """ + str(post.id) + " AND L.user_id != " +str(current_user.id) \
                    +" AND P.id = L.post_id"
        live_lists = db.session.execute(livequery)
        live = [(dict(j.items())) for j in live_lists]
    else: 
        current_live = Live.query.filter_by(user_id = current_user.id).filter_by(status = 3).first()
        if current_live is not None:
            # return all users who are lived with user
            livequery = """SELECT U.id, U.email, U.first_name, U.last_name, P.owner_id, U.username
                        FROM user AS U, lives AS L, posts AS P
                        WHERE L.user_id = U.id AND L.status = 3 AND
                        L.post_id = """ + str(current_live.post_id) + " AND L.user_id != " +str(current_user.id) \
                        +" AND P.id = L.post_id"
            live_lists = db.session.execute(livequery)
            live = [(dict(j.items())) for j in live_lists]
            other_post = Post.query.filter_by(id =current_live.post_id).first()
            if other_post is not None:
                if other_post.post_type:
                    other_post_on = On_campus.query.filter_by(post_id=other_post.id).first()
                else:
                    other_post_off = Off_campus.query.filter_by(post_id=other_post.id).first()

    # write the query to return current user's interested posts
    interestquery = """SELECT P.id, P.title, P.description, P.owner_id,
                        P.image_1, P.image_2, P.image_3
                       FROM posts AS P, lives AS L
                       WHERE L.post_id = P.id AND L.status = 1 AND L.user_id = """ + str(current_user.id)

    interests = db.session.execute(interestquery)
    interest = [(dict(i.items())) for i in interests]

    # return all of the ghost users who are following the current user
    ghostlive = Ghost_User.query.filter_by(representer_id = current_user.id).all()

    
    # write the query to return the post that user get approved
    approvequery = """SELECT P.id, P.title, P.description, P.owner_id,
                        P.image_1, P.image_2, P.image_3
                       FROM posts AS P, lives AS L
                       WHERE L.post_id = P.id AND L.status = 2 AND L.user_id = """ + str(current_user.id)

    approve_result = db.session.execute(approvequery)
    approves = [(dict(i.items())) for i in approve_result]
    
    return render_template('profile/profile.html', post = post, oncampus = oncampus,\
    live = live, interest =interest, offcampus=offcampus, wait_list=wait_list, \
    ghostlive = ghostlive, approves = approves, live_in_other = other_post,\
    live_in_other_on= other_post_on,live_in_other_off= other_post_off,title="My Profile")

@profile.route('/profile/<int:id>', methods=["GET"])
@login_required
def view_otherprofile(id):
    """
    View the given id user's profile
    """
    post = oncampus = offcampus = live = ghostlive = None
    user = User.query.filter_by(id = id).first()
    title = user.username + "Profile"
    post = Post.query.filter_by(owner_id=user.id).first()
    if post is not None:
        if post.post_type:
            oncampus = On_campus.query.filter_by(post_id=post.id).first()
        else:
            offcampus = Off_campus.query.filter_by(post_id=post.id).first()
    # return all users who are lived with post owner
        livequery = """SELECT U.id, U.email, U.first_name, U.last_name, P.owner_id, U.username
                    FROM user AS U, lives AS L, posts AS P
                    WHERE L.user_id = U.id AND L.status = 3 AND
                    L.post_id = """ + str(post.id) + " AND L.user_id != " +str(user.id) \
                    +" AND P.id = L.post_id"
        live_lists = db.session.execute(livequery)
        live = [(dict(j.items())) for j in live_lists]
    # return all of the ghost users who are following the current user
    ghostlive = Ghost_User.query.filter_by(representer_id = user.id).all()
    return render_template('profile/otherprofile.html', post = post, user = user, \
            oncampus= oncampus, offcampus= offcampus, live =live, \
            ghostlive= ghostlive, title = title)

@profile.route('/profile/accept_interest/<int:id1>/<int:id2>', methods=["GET"])
@login_required
def approve_interests(id1,id2):
    """
    Grant approval for user who is insterested in the post
    """
    live = Live.query.filter_by(post_id = id1).filter_by(user_id = id2).first()
    live.status = 2
    db.session.commit()
    return redirect(url_for('profile.ownprofile'), title="Other Profile")

@profile.route('/profile/accept_approval/<int:id1>', methods=["GET"])
@login_required
def accept_approval(id):
    """
    Accept interest
    """
    current_live = Live.query.filter_by(user_id = current_user.id).filter_by(status = 3).first()

    if current_live is not None:
        own_post = Post.query.filter_by(id= current_live.post_id)
        if own_post.owner_id == current_user.id:
            flash('Delete Your Post Before Accept the Approval')
            redirect(request.url)
        else:
            flash('Decline Your Accepted Post Before Accept the Approval')
            redirect(request.url)
    # check the space of the post
    q = Ghost_User.query.filter_by(representer_id = current_user.id).count()
    n = __spotTaken(id)
    current_post = Post.query.filter_by(id= id)
    live = Live.query.filter_by(post_id = id).filter_by(user_id = current_user.id).first()
    if live is not None and q + 1 + n > current_post.capacity:
        flash('Not enough spot')
        redirect(request.url)
    live.status = 3
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))

def __spotTaken(post):
    """
    Helper function to count the number of spots are taken
    """
    query = """SELECT COUNT(ghost_user.email) + COUNT(distinct(user.id))
                FROM users, ghost_user, lives
                WHERE ghost_user.representer_id = users.id
                    AND lives.user_id = users.id
                    AND lives.status = 3 AND lives.post_id = """ + str(post)            
    n = db.session.execute(query).scalar()
    return n

@profile.route('/profile/decline_interest/<int:id1>/<int:id2>', methods=["GET"])
@login_required
def decline_interests(id1,id2):
    """
    Decline the interest for user who is insterested in the post
    """
    live = Live.query.filter_by(post_id = id1).filter_by(user_id = id2).first()
    db.session.delete(live)
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))

@profile.route('/profile/remove_roommate/<int:id1>/<int:id2>', methods=["GET"])
@login_required
def remove_roommate(id1,id2):
    """
    Remove a roomate who accept the approve in current user's post
    """
    live = Live.query.filter_by(post_id = id1).filter_by(user_id = id2).first()
    db.session.delete(live)
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))

@profile.route('/profile/remove_interest/<int:id>', methods=['GET'])
@login_required
def remove_interest(id):
    """
    Remove current user's interests on a post
    """
    live = Live.query.filter_by(post_id = id).filter_by(user_id = current_user.id).first()
    db.session.delete(live)
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))


@profile.route('/profile/remove_ghost/<int:id>/<string:ghostemail>', methods=["GET"])
@login_required
def remove_ghost(id,ghostemail):
    """
    Remove user's Ghost roomates
    """
    ghost_user = Ghost_User.query.filter_by(representer_id = id).filter_by(email = ghostemail).first()
    db.session.delete(ghost_user)
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))