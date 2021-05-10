from core.db import db


class SaveableModel(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()
        db.session.refresh(self)