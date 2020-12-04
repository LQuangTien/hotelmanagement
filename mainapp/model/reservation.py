from sqlalchemy import and_

from mainapp.models import Reservation

def getByDate(start_date, end_date):
  return Reservation.query.filter(
      and_(Reservation.arriveDate >= start_date, Reservation.arriveDate <= end_date),
      and_(Reservation.departureDate >= start_date, Reservation.departureDate <= end_date)
    ).all()


def getAll():
  return Reservation.query.all()