from sqlalchemy import inspect

from factoryworldwide_app.server import db


class Base(db.Model):
    __abstract__ = True

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return None

    def update(self):
        try:
            db.session.commit()
            return self
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return None

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return None

    @classmethod
    def get(cls, key):
        try:
            return cls.query.get(key)
        except Exception as e:
            print(str(e))
            return None

    @classmethod
    def filter(cls, **kwargs):
        try:
            return cls.query.filter_by(**kwargs).first()
        except Exception as e:
            print(str(e))
            return None

    @classmethod
    def list(cls):
        try:
            return cls.query.all()
        except Exception as e:
            print(str(e))
            return None

