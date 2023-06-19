import os
import sqlalchemy as sa
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import UserMixin
from flask import url_for
from app import db

RATING_WORDS = {
    5: 'Отлично',
    4: 'Хорошо',
    3: 'Удовлетворительно',
    2: 'Неудовлетворительно',
    1: 'Плохо',
    0: 'Ужасно',
}

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)#unique=True
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

    def __repr__(self):
        return '<Category %r>' % self.name #name = строка с конкретным названием категории


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    last_name = db.Column(db.String(100), nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    middle_name = db.Column(db.String(100))
    login = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=sa.sql.func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name or ''])

    def __repr__(self):
        return '<User %r>' % self.login

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    short_desc = db.Column(db.Text, nullable=False)
    full_desc = db.Column(db.Text, nullable=False)
    rating_sum = db.Column(db.Integer, nullable=False, default=0)
    rating_num = db.Column(db.Integer, nullable=False, default=0)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    background_image_id = db.Column(db.String(100), db.ForeignKey('images.id'))
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())

    author = db.relationship('User')
    category = db.relationship('Category', lazy=False)
    bg_image = db.relationship('Image')

    def __repr__(self):
        return '<Course %r>' % self.name

    @property
    def rating(self):
        if self.rating_num > 0:
            return self.rating_sum / self.rating_num
        return 0
    
    def rating_up(self, n:int):
        self.rating_num += 1
        self.rating_sum += n

class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.String(100), primary_key=True)
    file_name = db.Column(db.String(100), nullable=False)
    mime_type = db.Column(db.String(100), nullable=False)
    md5_hash = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())
    object_id = db.Column(db.Integer)
    object_type = db.Column(db.String(100))

    def __repr__(self):
        return '<Image %r>' % self.file_name

    @property
    def storage_filename(self):
        _, ext = os.path.splitext(self.file_name)
        return self.id + ext

    @property
    def url(self):
        return url_for('image', image_id=self.id)

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=sa.sql.func.now())
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    course = db.relationship('Course')
    user = db.relationship('User')

    @property
    def rating_word(self):
        return RATING_WORDS.get(self.rating)

    def __repr__(self):
        return '<Review %r>' % self.id
# flask db migrate -m "comment"
# flask db upgrade

# User.query.all()
# User.query.get(user.id)
# User.query.first()
# User.query.filter_by(login='user').first()
# User.query.filter(User.login=='petrov').first()
# User.query.filter(User.login=='petrov').filter(User.role_id=='1').first() login = 'petrov AND role_id=='1'
# from sqlalchemy import and_, or_, not_
# User.query.filter(or_(User.login=='petrov').filter(User.role_id=='1')).all() login = 'petrov OR role_id=='1'
# query = User.query
# query = query.filter(User.login == 'user')
# query = query.filter(User.role_id == None)
# query.all()
# User.query.filter(not_(User.login.in_(['user', 'petrov']))).limit(10).all()