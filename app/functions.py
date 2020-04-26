from models import *
from app import db
from run import app
from sqlalchemy import text, func

'''
-Do we have to do try-catch around every commit?
-Make sure owner_id is both NOT NULL and UNIQUE.
'''

#-------------MY ACCOUNT & POST--------------#

# PROFILE SETUP (EDITS NOT ALLOWED, YET)

me = None
myPost = None

def newProfile(em, user, first, last, sex, college):
    # TODO: add the rest of the attrs
    global me
    me = User(email=em, username=user, first_name=first, last_name=last, is_admin=0, gender=sex, school=college)
    db.session.add(me)
    db.session.commit()
    db.session.refresh(me)
    return me

def addGhost(rep_id, em, first, last):
    '''@pre: the rep user is in User already'''
    if User.query.filter_by(email=em).scalar() is not None or Ghost_User.query.filter_by(email=em).scalar() is not None:
        return None
    # doesn't support adding ghost while already belong to a post yet
    ghost = Ghost_User(representer_id=rep_id, email=em, first_name=first, last_name=last)
    db.session.add(ghost)
    db.session.commit()
    return ghost

def logIn(em):
    '''retrieve everything about this user for other operations'''
    global me
    me = User.query.filter_by(email=em).one()
    myPost = Post.query.filter_by(user_id=me.id).one()


# MAKE/DELETE/MANAGE MY POST

def makePost(ptype, name, des, cap, img1, img2, img3):
    global myPost
    if Live.query.filter_by(user_id=me.id and status=3).scalar() is not None:
        return None # already in a post; can't create one
    post = Post(post_type=ptype, title=name, description=des, capacity=cap, image1=img1, image2=img2, image3=img3, owner_id=me.id)
    db.session.add(post)
    db.session.commit()
    db.session.refresh(post)

    live = Live(post_id=postID, user_id=me.id, status=2) # auto-approved
    db.session.add(live)
    db.session.commit()
    markAccepted(post.id)
    myPost = post
    return post

def makeOnCampus(id, col, d1, d2, d3, draw, n1, n2, n3, n4)
    post = On_campus(id, col, d1, d2, d3, drawNo, n1, n2, n3, n4)
    db.session.add(post)
    db.session.commit()
    return post

def deletePost():
    '''Delete my post'''
    db.session.delete(myPost)
    db.session.commit()
    myPost = None

def markApproved():
    live = Live.query.get((myPost.id, me.id))
    if live is None:
        return None # not supposed to happen, ever
    live.status = 2
    db.session.add(live)
    db.session.commit()
    return live

def incomingStatuses():
    return 0



#-------------NON-OWNER POST INTERACTIONS--------------#

# INTERACTIONS WITH POSTS

def markInterested(postID):
    live = Live(post_id=postID, user_id=me.id, status=1)
    db.session.add(live)
    db.session.commit()
    return live

def markAccepted(postID):
    '''@pre: post and live entries already exist'''
    if Live.query.filter_by(user_id=me.id and status=3).scalar() is not None:
        return None # already in a post; can't accept one
    q = Ghost_User.query.filter_by(repEmail = thisUser.email).count()
	post = Post.query.get(postID)
    live = Live.query.get((postID, me.id))
    n = spotTaken(post)
    if live is None or live.status != 2:
        return None # no relationship or not already approved
	if q + 1 + n <= post.capacity:
        live.status = 3
        db.session.commit()
        return live

def cancelInterest(postID):
    '''@pre: have pressed interest i.e. live entry exists with status==1'''
    Live.query.filter_by(post_id = postID and user_id = me.id).delete()
    db.session.commit()


def leavePost(postID):
    '''@pre: have a live entry with status 3 with this post'''
    if myPost is None: # can only leave as joiners, not owner
        Live.query.filter_by(post_id = postID and user_id = me.id).delete()
        db.session.commit()


# HELPER

def spotTaken(post):
    query = 'SELECT count(ghost_user.email) + count(distinct(user.id))'\
            'FROM users, ghost_user, lives'\
            'WHERE ghost_user.representer_id = users.id'\
            'and lives.user_id = users.id'\
            'and lives.post_id = ' + str(post)\
            'and lives.status = 2'
    n = db.session.execute(query).scalar()
    return n


# GET POSTS

postQuery = 'SELECT posts.*'\
	        'FROM lives, posts'\
	        'WHERE lives.post_id = posts.id'\
	        'and :myID = Live.user_id'\
	        'and lives.status == :state'

def getMyPost():
    return myPost

def getInterests():
    posts = db.session.query(Post).from_statement(text(query)).params(myID=me.id, state=1).all()
    return posts

def getApprovals():
    posts = db.session.query(Post).from_statement(text(query)).params(myID=me.id, state=2).all()
    return posts

def getOnCampus(postID):
    return On_campus.query.get(postID)

def getOffCampus(postID):
    return Off_campus.query.get(postID)