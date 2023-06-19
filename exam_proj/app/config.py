import os

SECRET_KEY = ''

SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://std_1861_exam_proj:@std-mysql.ist.mospolytech.ru/std_1861_exam_proj'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')
