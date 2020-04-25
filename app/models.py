# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class User(UserMixin, db.Model):
    """
    Create an User table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    gender = db.Column(db.Boolean)
    school = db.Column(db.Integer, index=True)
    pets = db.relationship('Pet', backref='user', lazy=True)
    is_smoke = db.Column(db.Boolean)
    allergies = db.relationship('Allergy', backref='user', lazy=True)
    has_car = db.Column(db.Boolean)
    has_bike = db.Column(db.Boolean)
    noise_Sen = db.Column(db.Integer)
    wakeup = db.Column(db.Integer)
    bedtime = db.Column(db.Integer)
    partyFreq = db.Column(db.Integer)
    visitorFreq = db.Column(db.Integer)
    post_id = db.relationship('Post', backref='user', lazy=True)
    status = db.relationship('Live', backref='user', uselist=False)
    ghost_users = db.relationship('Ghost_User', backref='user', lazy=True)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.username)
        


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Pet(db.Model):
    """
    Create a Pet table
    """

    __tablename__ = 'pets'

    name = db.Column(db.String(60), primary_key=True)
    #description = db.Column(db.String(200), nullable=True) #should we add description?
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False, primary_key=True)

    def __repr__(self):
        return '<Pet: {}>'.format(self.name)

class Allergy(db.Model):
    """
    Create a Pet table
    """

    __tablename__ = 'allergies'

    name = db.Column(db.String(60), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False, primary_key=True)

    def __repr__(self):
        return '<Allergy: {}>'.format(self.name)

class Post(db.Model):
    """
    Create a Post table
    """

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.Boolean, default=True, index=True)
    #True for on campus post, and False for off-campus post 
    allows_pet = db.Column(db.Boolean, default=False, nullable = False)
    allowed_gender = db.Column(db.Integer, default = 2, nullable = False)
    title = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    capacity = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable =False)
    image_1 = db.Column(db.LargeBinary)
    image_2 = db.Column(db.LargeBinary)
    image_3 = db.Column(db.LargeBinary)
    lives = db.relationship('Live', backref= 'posts', lazy=True)

    def __repr__(self):
        return '<Post: {}>'.format(self.id)

class Ghost_User(db.Model):
    """
    Create a Ghost_User table
    """
    __tablename__ = 'ghost_user'

    representer_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False, primary_key=True)
    email = db.Column(db.String(60), unique=True, primary_key=True)
    first_name = db.Column(db.String(60), nullable=False)
    last_name = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return '<Ghost_User: {}>'.format(self.email)

# class Image(db.Model):
#     """
#     Create a Image table
#     """
#     __tablename__ = 'images'

#     id = db.Column(db.Integer, primary_key=True)
#     images = db.Column(db.LargeBinary)
#     post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)

#     def __repr__(self):
#         return '<Images: {}>'.format(self.id)

class On_campus(db.Model):
    """
    Create a on campus table
    """
    __tablename__ = 'oncampus'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
    college = db.Column(db.Integer, nullable=False)
    dorm_1 = db.Column(db.String(60))
    dorm_2 = db.Column(db.String(60))
    dorm_3 = db.Column(db.String(60))
    drawNo = db.Column(db.Integer)
    nSingles = db.Column(db.Integer, index=True, default = 0)
    nDoubles = db.Column(db.Integer, index=True, default = 0)
    nTriples = db.Column(db.Integer, index=True, default = 0)
    nQuads = db.Column(db.Integer, index=True, default = 0)
    
    def __repr__(self):
        return '<On campus: {}>'.format(self.college, self.dorm_1, self.drawNo)

class Off_campus(db.Model):
    """
    Create a off campus table
    """
    __tablename__ = 'offcampus'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
    price = db.Column(db.Integer)
    street = db.Column(db.String(100))
    city = db.Column(db.String(60), index = True, nullable =False)
    state = db.Column(db.String(60), index = True, nullable =False )
    zipcode = db.Column(db.String(5))
    nParking = db.Column(db.Integer, default= 0)
    nRoom = db.Column(db.Integer, default = 0)
    nBathroom = db.Column(db.Integer, default = 0)
    nKitchen = db.Column(db.Integer, default = 0)
    size = db.Column(db.Integer, default = 0)
    pet_allowed = db.Column(db.Boolean, default=False)
    substance_free = db.Column(db.Boolean, default=False)
    ac = db.Column(db.Boolean, default=False)
    laundry = db.Column(db.Boolean, default=False)
    dishwasher = db.Column(db.Boolean, default=False)
    url = db.Column(db.String(100))

    def __repr__(self):
        return '<Off campus: {}>'.format(self.price)

class Live(db.Model):
    """
    Create a Live table
    """
    
    __tablename__ = 'lives'

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    status = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return '<Off campus: {}>'.format(self.status)
