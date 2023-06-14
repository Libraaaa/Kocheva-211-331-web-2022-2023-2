from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from app import db
from models import Course, Category, User, Grade, Review
from tools import CoursesFilter, ImageSaver
import sqlalchemy as sa

bp = Blueprint('courses', __name__, url_prefix='/courses')

PER_PAGE = 3

COURSE_PARAMS = [
    'author_id', 'name', 'category_id', 'short_desc', 'full_desc'
]

def params():
    return { p: request.form.get(p) for p in COURSE_PARAMS }

def search_params():
    return {
        'name': request.args.get('name'),
        'category_ids': request.args.getlist('category_ids'),
    }


@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    courses = CoursesFilter(**search_params()).perform()
    pagination = courses.paginate(page, PER_PAGE)
    courses = pagination.items
    categories = Category.query.all()
    return render_template('courses/index.html',
                           courses=courses,
                           categories=categories,
                           pagination=pagination,
                           search_params=search_params())

@bp.route('/new')
def new():
    categories = Category.query.all()
    users = User.query.all()
    return render_template('courses/new.html',
                           categories=categories,
                           users=users)

@bp.route('/create', methods=['POST'])
def create():
    f = request.files.get('background_img')
    if f and f.filename:
        img = ImageSaver(f).save()
        
    try:
        course = Course(**params(), background_image_id=img.id)
        db.session.add(course)
        db.session.commit()
        flash(f'Курс {course.name} был успешно добавлен!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'При сохранения курса произошла ошибка', 'danger')
        db.session.rollback()
        categories = Category.query.all()
        users = User.query.all()
        return render_template('courses/new.html',
                        categories=categories,
                        users=users)
    return redirect(url_for('courses.index'))

@bp.route('/<int:course_id>')
def show(course_id):
    course = Course.query.get(course_id)
    user_review = Review()
    if current_user.is_authenticated:
        user_review = Review.query.filter_by(user_id=current_user.id).filter_by(course_id=course_id).first()
    course_reviews = Review.query.filter_by(course_id=course_id).order_by(Review.created_at.desc()).limit(5).all()
    return render_template('courses/show.html', course=course, 
                           review=user_review, course_reviews=course_reviews)

@bp.route('/<int:course_id>/give_review')
def give_review(course_id):
    course = Course.query.get(course_id)
    user = User.query.get(current_user.id)
    grades = Grade.query.all()
    return render_template('courses/give_review.html',
                           course=course,
                           user = user,
                           grades=grades)

@bp.route('/<int:course_id>/send', methods=['POST'])
def send_review(course_id):
    try:
        text = request.form.get('text_review')
        grade = int(request.form.get('grade_id'))
        review = Review(text=text, rating=grade, course_id=course_id, user_id=current_user.id)
        db.session.add(review)
        course = Course.query.get(course_id)
        course.rating_up(grade-1)
        db.session.commit()
        flash(f'Ваш отзыв был успешно отправлен!', 'success')

    except sa.exc.SQLAlchemyError:
        flash(f'При отправке отзыва произошла ошибка', 'danger')
        db.session.rollback()
        course = Course.query.get(course_id)
        user = User.query.get(current_user.id)
        grades = Grade.query.all()
        return render_template('courses/give_review.html',
                           course=course,
                           user = user,
                           grades=grades)
    return redirect(url_for('courses.show', course_id = course_id))

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    page = request.args.get('page', 1, type=int)
    course_reviews = Review.query.filter_by(course_id=course_id)
    sort_reviews = request.args.get('sort_reviews')
    dictionary_reviews={'reviews_filter': sort_reviews, 'course_id': course_id}
    if sort_reviews == 'positive':
        course_reviews = course_reviews.order_by(Review.rating.desc())
    elif sort_reviews == 'negative':
        course_reviews = course_reviews.order_by(Review.rating.asc())
    else:
        course_reviews = course_reviews.order_by(Review.created_at.desc())
    pagination = course_reviews.paginate(page, 5)
    course_reviews = pagination.items
    return render_template('courses/reviews.html', 
                            course_reviews=course_reviews, course_id=course_id,
                            pagination=pagination, params = dictionary_reviews)
