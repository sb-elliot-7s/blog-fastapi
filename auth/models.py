from datetime import datetime
from database import Base
import sqlalchemy as _sql
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = 'users'

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    username = _sql.Column(_sql.String(length=255), nullable=True)
    email = _sql.Column(_sql.String, unique=True)
    password = _sql.Column(_sql.String)
    bio = _sql.Column(_sql.String(length=255), nullable=True)
    is_active = _sql.Column(_sql.Boolean, default=True)
    created = _sql.Column(_sql.DateTime, default=datetime.now)
    updated = _sql.Column(_sql.DateTime, default=datetime.now, onupdate=datetime.now)

    articles = relationship('Article', backref='user', cascade='all, delete')

    def __repr__(self) -> str:
        return f'<User: {self.id} {self.username}>'

