from sqlalchemy import and_, desc

from mainapp import db
from mainapp.models import Reservation

def getByUserId(userId):
  return Reservation.query.filter(Reservation.user == userId).order_by(desc(Reservation.id)).all()


def getByDate(start_date, end_date):
  return Reservation.query.filter(
      and_(Reservation.arriveDate >= start_date, Reservation.arriveDate <= end_date),
      and_(Reservation.departureDate >= start_date, Reservation.departureDate <= end_date)
    ).all()


def getAll():
  return Reservation.query.all()

def create(reservationData):
  reservation = Reservation(room=reservationData['room'], user=reservationData['user'], arriveDate=reservationData['arriveDate'],
              departureDate=reservationData['departureDate'], dayTotal=reservationData['dayTotal'], numberOfGuest=reservationData['numberOfGuest'],
              hasForeigner=reservationData['hasForeigner'], isOverCapacity=reservationData['isOverCapacity'], tax=reservationData['tax'], total=reservationData['total'])
  db.session.add(reservation)
  db.session.commit()
  return reservation