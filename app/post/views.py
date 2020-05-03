# app/post/views.py

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from . import post
from .. import db
from ..models import Post, On_campus, User, Live, On_campus, Off_campus

@post.route('/oncampus', methods=['GET', 'POST'])
@login_required
def list_oncampuspost():
    """
    List all posts which statisfy the conditions
    """
    if request.method == 'POST':
        query = """SELECT P.id, P.post_type, P.allows_pet, P.allowed_gender, P.title,
        P.description, P.capacity, P.owner_id, P.image_1, O.college, O.dorm_1,
         O.dorm_2, O.dorm_3, O.drawNo, O.nSingles, O.nDoubles,
         O.nTriples, O.nQuads, U.username 
         FROM user As U, posts As P, oncampus As O
         WHERE P.post_type = 1 AND U.id = P.owner_id AND P.id = O.post_id"""
        if request.form['school'] != "0":
            query = query + " AND O.college = "+ request.form['school']
        if request.form['pet'] != "2":
            query = query + " AND P.allows_pet = " + request.form['pet']
        if request.form['capacity'] != "0":
            query = query + " AND P.capacity= " + request.form['capacity']
        if request.form["nSingles"] != "0":
            query = query + " AND O.nSingles = " + request.form['nSingles']
        if request.form["nDoubles"] != "0":
            query = query + " AND O.nDoubles = " + request.form['nDoubles']
        if request.form["nTriples"] != "0":
            query = query + " AND O.nTriples = " + request.form['nTriples']
        if request.form["nQuads"] != "0":
            query = query + " AND O.nQuads = " + request.form['nQuads']
        if request.form['partyFreq'] != "0":
            query = query + " AND U.partyFreq <= " + request.form['partyFreq']
        if request.form['visitorFreq'] != "0":
            query = query +" AND U.visitorFreq <= " + request.form['visitorFreq']
        if request.form['wakeup'] != "0":
            query = query +" AND U.wakeup = " + request.form['wakeup']
        if request.form["bedtime"] != "0":
            query = query +" AND U.bedtime = " + request.form['bedtime']
        if request.form["noiseSen"] != "0":
            query = query +" AND U.noise_Sen <= " + request.form['noiseSen']
        if request.form["allowed_gender"] != "0":
            query = query + " AND P.allowed_gender = " + request.form['allowed_gender']
        query = query + """ AND NOT EXISTS (SELECT 1 FROM lives WHERE lives.post_id = P.id
                 AND lives.user_id = """ + str(current_user.id) +");"
        posts = db.session.execute(query)

        # print(query, type(request.form['capacity']))
        rows = [(dict(row.items())) for row in posts]
        return render_template('post/oncampus.html', posts = rows, title = 'On Campus Filtering')

    # if request.method == 'GET' - mark user as interested
    return render_template('post/oncampus.html', posts = None, title = 'On Campus Filtering')
  
@post.route('/make_post', methods=['GET'])
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
    if request.method == "POST":
        return redirect(url_for('profile.ownprofile'))
    return render_template('post/make_post_offcampus.html', title="Make a Post")

@post.route('/make-post-oncampus-suite',methods=['GET','POST'])
@login_required
def make_post_oncampus_suite():
    """
    Render the page to make a post for on-campus suite housing
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        allows_pet = bool(request.form['allows_pet'])
        allowed_gender = int(request.form['allowed_gender'])
        nSingles=int(request.form['nSingles'])
        nDoubles=int(request.form['nDoubles'])
        nTriples=int(request.form['nTriples'])
        nQuads=int(request.form['nQuads'])
        drawNo=int(request.form['drawNo'])
        dorm1 = request.form['dorm1']
        dorm2 = request.form['dorm2']
        dorm3 = request.form['dorm3']
        school = request.form['school']
        capacity = nSingles + 2*nDoubles + 3*nTriples + 4*nQuads

        img1blob = img2blob = img3blob= None

        img1 = request.files["image1"]
        img2 = request.files["image2"]
        img3 = request.files["image3"]
        if img1:   
            if not allowed_file(img1.filename):
                flash("The file type for image one is wrong.")
                return redirect(request.url)
            else:
                img1blob = img1.read()
        if img2: 
            if not allowed_file(img2.filename):
                flash("The file type for image two is wrong.")
                return redirect(request.url)
            else:
                img1blob = img2.read()
        if img3:          
            if not allowed_file(img3.filename):
                flash("The file type for image three is wrong.")
                return redirect(request.url)
            else:
                img1blob = img3.read()
        post = Post(post_type = 1, allows_pet = allows_pet, allowed_gender= allowed_gender,\
            title = title, description= description, capacity = capacity, owner_id = current_user.id,\
            image_1=img1blob, image_2=img2blob, image_3=img3blob)
        db.session.add(post)
        db.session.commit()
        last = Post.query.filter_by(owner_id= current_user.id).filter_by(post_type =1).first()
        oncampus = On_campus(post_id= last.id, college = school, dorm_1=dorm1, dorm_2=dorm2,\
            dorm_3=dorm3, nSingles=nSingles, nDoubles=nDoubles,nTriples=nTriples,nQuads=nQuads, drawNo= drawNo)
        db.session.add(oncampus)
        live = Live(post_id=last.id, user_id = current_user.id, status=3)
        db.session.add(live)
        db.session.commit()
        return redirect(url_for('profile.ownprofile'))
    return render_template('post/make_post_oncampus_suite.html', title="Make a Post")

@post.route('/make-post-oncampus-room',methods=['GET','POST'])
@login_required
def make_post_oncampus_room():
    """
    Render the page to make a post for on-campus room housing
    """
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        allows_pet = bool(request.form['allows_pet'])
        allowed_gender = int(request.form['allowed_gender'])
        nSingles= nDoubles = nTriples = nQuads = 0
        roomtype = request.form['roomType']
        if roomtype == 'Double':
            nDoubles = 1
        if roomtype == 'Triple':
            nTriples = 1
        if roomtype == 'Quads':
            nQuads = 1
        drawNo=int(request.form['drawNo'])
        dorm1 = request.form['dorm1']
        dorm2 = request.form['dorm2']
        dorm3 = request.form['dorm3']
        school = request.form['school']
        capacity = 2*nDoubles + 3*nTriples + 4*nQuads

        img1blob = img2blob = img3blob= None

        img1 = request.files["image1"]
        img2 = request.files["image2"]
        img3 = request.files["image3"]
        if img1:   
            if not allowed_file(img1.filename):
                flash("The file type for image one is wrong.")
                return redirect(request.url)
            else:
                img1blob = img1.read()
        if img2: 
            if not allowed_file(img2.filename):
                flash("The file type for image two is wrong.")
                return redirect(request.url)
            else:
                img1blob = img2.read()
        if img3:          
            if not allowed_file(img3.filename):
                flash("The file type for image three is wrong.")
                return redirect(request.url)
            else:
                img1blob = img3.read()
        post = Post(post_type = 1, allows_pet = allows_pet, allowed_gender= allowed_gender,\
            title = title, description= description, capacity = capacity, owner_id = current_user.id,\
            image_1=img1blob, image_2=img2blob, image_3=img3blob)
        db.session.add(post)
        db.session.commit()
        last = Post.query.filter_by(owner_id= current_user.id).filter_by(post_type =1).first()
        oncampus = On_campus(post_id= last.id, college = school, dorm_1=dorm1, dorm_2=dorm2,\
            dorm_3=dorm3, nSingles=nSingles, nDoubles=nDoubles,nTriples=nTriples,nQuads=nQuads, drawNo= drawNo)
        db.session.add(oncampus)
        live = Live(post_id=last.id, user_id = current_user.id, status=3)
        db.session.add(live)
        db.session.commit()
        return redirect(url_for('profile.ownprofile'))
    return render_template('post/make_post_oncampus_room.html', title="Make a Post")

@post.route('/delete_post/<int:id>')
@login_required
def delete_post(id):
    """
    Delete current user's post and clean up the live table
    """
    live = Live.query.filter_by(post_id= id).all()
    oncampus = On_campus.query.filter_by(post_id= id).first()
    offcampus = Off_campus.query.filter_by(post_id= id).first()
    if live is not None:
        for people in live:
            db.session.delete(people)
    if oncampus is not None:
        db.session.delete(oncampus)
    if offcampus is not None:
        db.session.delete(offcampus)
    post = Post.query.filter_by(id = id).first()
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))

@post.route('/post/like_post/<int:id>', methods=["GET"])
@login_required
def like_post(id):
    """
    Remove current user's interests on a post
    """
    temp = Live.query.filter_by(post_id = id).filter_by(user_id = current_user.id).first()
    if  temp is not None:
        flash("You have liked this Post")
        return redirect(url_for('post.list_oncampuspost'))
    like = Live(post_id = id, user_id = current_user.id, status = 1)
    db.session.add(like)
    db.session.commit()
    return redirect(url_for('profile.ownprofile'))
# allowed image types
ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'png'])

def allowed_file(filename):
    """Takes in a string as the input and check filename extension
        Return true if filename have correct extensions
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS