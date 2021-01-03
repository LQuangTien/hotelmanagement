from sqlalchemy import or_, func

from mainapp import db
from mainapp.models import Room, RoomType, Reservation


# ROOM_ROOMTYPE = db.session.query(Room, RoomType).join(RoomType, Room.type == RoomType.id)
# ROOM_ROOMTYPE_RESERVATION = db.session.query(Room, RoomType, Reservation)
# JOINED_TABLE = ROOM_ROOMTYPE_RESERVATION.join(RoomType, Room.type == RoomType.id)
# LEFTJOINED_TABLE = JOINED_TABLE.outerjoin(Reservation, Room.id == Reservation.room)


def getAll():
    ROOM_ROOMTYPE_RESERVATION = db.session.query(Room, RoomType, Reservation)
    JOINED_TABLE = ROOM_ROOMTYPE_RESERVATION.join(RoomType, Room.type == RoomType.id)
    return JOINED_TABLE.group_by(Room.id).order_by(Room.name).all()


def get(name):
    ROOM_ROOMTYPE = db.session.query(Room, RoomType).join(RoomType, Room.type == RoomType.id)
    roomInfo, typeInfo = ROOM_ROOMTYPE.filter(Room.name == name).first()
    return roomInfo, typeInfo


def getByDate(type=None, arriveDate=None, departureDate=None):
    ROOM_ROOMTYPE = db.session.query(Room, RoomType).join(RoomType, Room.type == RoomType.id)

    bookedRoomBasedOnTime = db.session.query(Reservation.room).filter(
        or_(func.DATE(arriveDate).between(Reservation.arriveDate, Reservation.departureDate),
            func.DATE(departureDate).between(Reservation.arriveDate, Reservation.departureDate)
            )
    )

    result = ROOM_ROOMTYPE.filter(
        (Room.type == type),
        Room.id.notin_(bookedRoomBasedOnTime)
    ) \
        if type \
        else ROOM_ROOMTYPE.filter(Room.id.notin_(bookedRoomBasedOnTime))

    return result.group_by(Room.id).all()
