import hashlib
import uuid
import os
from werkzeug.utils import secure_filename
from models import Course, Image, Review
from app import db, app
import sqlalchemy as sa

class CoursesFilter:
    def __init__(self, name, category_ids):
        self.name = name
        self.category_ids = category_ids if 'all' not in category_ids else None
        self.query = Course.query

    def perform(self):
        self.__filter_by_name()
        self.__filter_by_category_ids()
        return self.query.order_by(Course.created_at.desc())

    def __filter_by_name(self):
        if self.name:
            self.query = self.query.filter(
                Course.name.ilike('%' + self.name + '%'))

    def __filter_by_category_ids(self):
        if self.category_ids:
            self.query = self.query.filter(
                Course.category_id.in_(self.category_ids))

class ImageSaver:
    def __init__(self, file):
        self.file = file

    def save(self):
        self.img = self.__find_by_md5_hash()
        if self.img is not None:
            return self.img
        file_name = secure_filename(self.file.filename)
        self.img = Image(
            id=str(uuid.uuid4()),
            file_name=file_name,
            mime_type=self.file.mimetype,
            md5_hash=self.md5_hash)
        try:
            self.file.save(
                os.path.join(app.config['UPLOAD_FOLDER'],
                            self.img.storage_filename))
            db.session.add(self.img)
            db.session.commit()
        except sa.exc.SQLAlchemyError:
            db.session.rollback()
            return None
        except:
            db.session.delete(self.img)
            db.session.commit()
            return None
        return self.img

    def __find_by_md5_hash(self):
        self.md5_hash = hashlib.md5(self.file.read()).hexdigest()
        self.file.seek(0)
        return Image.query.filter(Image.md5_hash == self.md5_hash).first()
