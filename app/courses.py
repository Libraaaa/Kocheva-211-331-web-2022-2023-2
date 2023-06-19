from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from app import db
from models import Course, Category, User, Review
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
    # print('='*30, "\n", search_params(), "\n", '='*30)
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

@bp.route('/<int:course_id>/new review', methods=['POST'])
@login_required
def new_review(course_id): #user petrov kykyshkin alex rogov flower yulay
    user_id = current_user.id
    check_review = Review.query.filter_by(course_id=course_id).filter_by(user_id=user_id).all()
    if check_review:
        flash(f'Вы уже оставляли отзыв на этот курс.', 'warning')
        return redirect(url_for('courses.show', course_id=course_id))
    text = request.form['text']
    rating = request.form['rating']
    review = Review(text=text, rating=rating, 
                    course_id=course_id, user_id=user_id)
    try:
        db.session.add(review)
        course = Course.query.get(course_id)
        course.rating_up(int(rating))
        db.session.commit()
        flash(f'Отзыв успешно добавлен', 'success')
    except:
        db.session.rollback()
        flash(f'При сохранении отзыва произошла ошибка', 'success')
    # print(user_id, course_id, text, rating, review)
    return redirect(url_for('courses.show', course_id=course_id))

@bp.route('/<int:course_id>/reviews')
def reviews(course_id):
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(course_id=course_id)
    reviews_filter = request.args.get('reviews_filter')
    d={'reviews_filter': reviews_filter, 'course_id': course_id}
    if reviews_filter == 'by_pos':
        reviews = reviews.order_by(Review.rating.desc())
    elif reviews_filter == 'by_neg':
        reviews = reviews.order_by(Review.rating.asc())
    else:
        reviews = reviews.order_by(Review.created_at.desc())
    pagination = reviews.paginate(page, 5)
    reviews = pagination.items
    return render_template('courses/reviews.html', 
                           course_reviews=reviews, course_id=course_id, 
                           pagination=pagination, search_params = d)