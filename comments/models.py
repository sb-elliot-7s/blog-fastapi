from database import Base
import sqlalchemy as _sql

from datetime import datetime


class Comment(Base):
    __tablename__ = "comments"

    id = _sql.Column(_sql.Integer, primary_key=True, index=True)
    text = _sql.Column(_sql.String)
    article_id = _sql.Column(_sql.Integer, _sql.ForeignKey("articles.id"))
    user_id = _sql.Column(_sql.Integer, _sql.ForeignKey("users.id"))
    created = _sql.Column(_sql.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"<Comment: {self.text[:50]}>"
