from flask import session
from datetime import datetime
from mainapp.model import room, user
from mainapp.utils import subtractDate

SECONDS_IN_ONE_DAY = 60*60*24

def bookingRoom(request):
  roomName = int(request.form.get("roomName"))
  roomInfo, typeInfo = room.get(roomName)
  userId = session.get('user')
  currentUser = user.get(userId)
  bookForm = session.get('bookForm')
  arriveDate = bookForm['arriveDate']
  departureDate = bookForm['departureDate']
  numberOfGuest = bookForm['numberOfGuest']
  hasForeigner = bookForm['hasForeigner']
  dayTotal = subtractDate(departureDate, arriveDate)/SECONDS_IN_ONE_DAY

  session['booking'] = {
    "room": roomInfo.name,
    "sex": currentUser.sex,
    "image": roomInfo.image,
    "price": typeInfo.price,
    "arriveDate": arriveDate,
    "dayTotal": int(dayTotal),
    "email": currentUser.email,
    "hasForeigner": hasForeigner,
    "address": currentUser.address,
    "numberOfGuest": numberOfGuest,
    "departureDate": departureDate,
    "lastname": currentUser.lastname,
    "firstname": currentUser.firstname,
  }
  return session['booking']