from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    name = Column(String(20), nullable=False)
    email = Column(String(40), index=True, nullable=False)
    password_hash = Column(String(100), nullable=False)

    def set_password(self, password):
        self.password_hash = password

    def check_password(self, password):
        return self.password_hash == password


class RefUserMixin:
    @declared_attr
    def user_id(cls):
        return Column('user_id', ForeignKey('users.id'), nullable=False)

    @declared_attr
    def user(cls):
        return relationship("User", backref=backref(cls.__tablename__, lazy='dynamic'))
