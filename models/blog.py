from sqlalchemy import Column, String, Text

from .base import Base, TimestampMixin
from .user import RefUserMixin


class Entry(Base, TimestampMixin, RefUserMixin):
    title = Column(String(40), nullable=False)
    body = Column(Text, nullable=False)


class Tag(Base, RefUserMixin):
    name = Column(String(20), unique=True, index=True, nullable=False)
