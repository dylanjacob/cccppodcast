# services/rsspy/lib/api/models.py


from sqlalchemy.sql import func

from lib import db


class Episode(db.Model):

    __tablename__ = 'episodes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    summary = db.Column(db.Text(), nullable=False)
    media = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, title, summary, media):
        """Initialize object."""
        self.title = title
        self.summary = summary
        self.media = media

    def to_json(self):
        """Return a JSON representation of the object."""
        return {
            'id': self.id,
            'title': self.title,
            'summary': self.summary,
            'media': self.media,
            'active': self.active,
            'created_date': self.created_date
        }
