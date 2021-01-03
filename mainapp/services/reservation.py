from flask import session
from mainapp.model import reservation

def create(bookingInfo):
  userId = session.get('user')
  reservationData = {
    'room': bookingInfo['roomId'],
    'user': userId,
    'arriveDate': bookingInfo['arriveDate'],
    'departureDate': bookingInfo['departureDate'],
    'dayTotal': bookingInfo['dayTotal'],
    'numberOfGuest': bookingInfo['numberOfGuest'],
    'hasForeigner': bookingInfo['hasForeigner'],
    'isOverCapacity': bookingInfo['isOverCapacity'],
    'tax': bookingInfo['tax'],
    'total': int(bookingInfo['dayTotal'] * float(bookingInfo['tax']) * bookingInfo['price']),
  }
  return reservation.create(reservationData)
