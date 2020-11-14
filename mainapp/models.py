from flask_login import UserMixin
from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy import Enum
from sqlalchemy.orm import relationship
from mainapp import db
from datetime import datetime


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    email = Column(String(50), nullable=True, unique=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    address = Column(String(100), nullable=True)
    sex = Column(Enum('Male', 'Female', 'Other'))
    isActive = Column(Boolean, default=True)
    isAdmin = Column(Boolean, default=False)
    def __str__(self):
        return self.username


class Room(db.Model):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Integer, nullable=False, unique=True)
    arriveDate = Column(Date, default=datetime.now())
    departureDate = Column(Date, default=datetime.now())
    price = Column(Integer, nullable=False)
    capacity = Column(Enum('2', '4'), nullable=False)
    image = Column(String(50), nullable=False)
    description = Column(String(1000), nullable=False)
    isBooked = Column(Boolean, default=False)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    db.create_all()
