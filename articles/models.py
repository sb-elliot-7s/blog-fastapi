import sqlalchemy as _sql
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
from auth.models import User
from comments.models import Comment


class Article(Base):
    __tablename__ = "articles"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    title = _sql.Column(_sql.String(length=255))
    content = _sql.Column(_sql.String)
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    updated = _sql.Column(_sql.DateTime, default=datetime.now, onupdate=datetime.now)
    comments = relationship("Comment", backref="article", cascade='all, delete', lazy='joined')
    images = relationship('Image', backref="article", cascade="all, delete", lazy='joined')

    def __repr__(self) -> str:
        return f"<Article: {self.id} - {self.title}:: {self.user.username or self.user.id}>"


class Image(Base):
    __tablename__ = 'images'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    article_id = _sql.Column(_sql.Integer, _sql.ForeignKey('articles.id'))
    photo = _sql.Column(_sql.String, nullable=True, unique=True)

    def __repr__(self) -> str:
        return f'<Image: {self.photo}>'
