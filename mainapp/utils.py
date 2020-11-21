from datetime import date, datetime
from pprint import pprint

from sqlalchemy import or_, and_, func, cast, Date, not_

from mainapp import db
from mainapp.models import Room, RoomType, Reservation


def getAll_room(type=None, arriveDate=None, departureDate=None):
    return db.session.query(Room, RoomType, Reservation) \
        .join(RoomType, Room.type == RoomType.id) \
        .outerjoin(Reservation, Room.id == Reservation.room) \
        .filter(
            (Room.type == type),
            or_(
                not_(Reservation.arriveDate.between(arriveDate, departureDate)),
                Reservation.arriveDate == None
            ),
            or_(
                not_(Reservation.departureDate.between(arriveDate, departureDate)),
                Reservation.departureDate == None
            ),
        ) \
        .all() \
        if type  \
        else db.session.query(Room, RoomType, Reservation) \
        .join(RoomType, Room.type == RoomType.id) \
        .outerjoin(Reservation, Room.id == Reservation.room) \
        .filter(
            or_(
                not_(Reservation.arriveDate.between(arriveDate, departureDate)),
                Reservation.arriveDate == None
            ),
            or_(
                not_(Reservation.departureDate.between(arriveDate, departureDate)),
                Reservation.departureDate == None
            ),
        ) \
        .all() \

