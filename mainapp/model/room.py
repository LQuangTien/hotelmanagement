from sqlalchemy import or_, func, not_

from mainapp import db
from mainapp.models import Room, RoomType, Reservation

JOINED_TABLE = db.session.query(Room, RoomType, Reservation) \
            .join(RoomType, Room.type == RoomType.id)
LEFTJOINED_TABLE = JOINED_TABLE.outerjoin(Reservation, Room.id == Reservation.room)


def getAll():
    return JOINED_TABLE.group_by(Room.id).order_by(Room.name).all()


def getByQuery(type=None, arriveDate=None, departureDate=None):
    bookedRoomBasedOnTime = db.session.query(Reservation.room).filter(
        or_(func.DATE(arriveDate).between(Reservation.arriveDate, Reservation.departureDate),
            func.DATE(departureDate).between(Reservation.arriveDate, Reservation.departureDate)
            )
    )

    result = LEFTJOINED_TABLE.filter(
        (Room.type == type),
        Room.id.notin_(bookedRoomBasedOnTime)
    ) \
        if type \
        else LEFTJOINED_TABLE.filter(Room.id.notin_(bookedRoomBasedOnTime))

    return result.group_by(Room.id).all()
