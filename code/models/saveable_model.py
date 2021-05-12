from core.db import db


class SaveableModel(db.Model):
    __abstract__ = True

    def save(self, session=None, commit=False):
        # When not session not provided, use the default session
        if session is None:
            session = db.session
        session.add(self)
        if commit:
            session.commit()
        else:
            session.flush()
        session.refresh(self)