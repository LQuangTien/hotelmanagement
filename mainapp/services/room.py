from math import ceil
from flask import session
from mainapp import utils
from werkzeug.utils import redirect
from mainapp.utils import subtractDate
from mainapp.services import reservation

from mainapp.model import room, roomtype, user, regulation


SECONDS_IN_ONE_DAY = 60*60*24

def getRoomTypes():
  maxCapacity =  int(regulation.getAll()[0].value)
  return [type.name for type in roomtype.getAll()], maxCapacity

def handlePostBooking(request):
  bookingInfo = bookingRoom(request)
  amount = float(bookingInfo['tax']) * bookingInfo['price'] * bookingInfo['dayTotal']
  qrURL = utils.createQRCode(int(amount))
  session['booking']['qrURL'] = qrURL
  return bookingInfo, qrURL

def handleGetBooking(request):
  bookingInfo = session.get('booking')
  if (not bookingInfo):
    return redirect('/')
  qrURL = bookingInfo['qrURL'] or None
  errorCode = request.args.get('errorCode') or None
  if (errorCode):
    bookingInfo['isDone'] = True
  if (bookingInfo['isDone']):
    reservation.create(bookingInfo)
    session['booking'] = None
    session['bookForm'] = None
  return bookingInfo, qrURL, errorCode

def getAll():
  rooms = room.getAll()
  perPage = 3
  totalPage = ceil(len(rooms) / perPage)
  return rooms, perPage, totalPage

def handleGetRooms(request):
  type = None if request.args.get('type') == 'Any' else request.args.get('type')
  arriveDate = request.args.get('arriveDate')
  departureDate = request.args.get('departureDate')
  numberOfGuest = int(request.args.get("numberOfGuest"))
  hasForeigner = request.args.get("hasForeigner")
  hasForeigner = True if hasForeigner == 'True' else False
  session['bookForm'] = {
    "arriveDate": arriveDate,
    "departureDate": departureDate,
    "numberOfGuest": numberOfGuest,
    "hasForeigner": hasForeigner,
    "type": type,
  }
  return type, arriveDate, departureDate

def getByDate(type, arriveDate, departureDate):
  rooms = room.getByDate(type, arriveDate, departureDate)
  perPage = 3
  totalPage = ceil(len(rooms) / perPage)
  return rooms, perPage, totalPage

def bookingRoom(request):

  LIMIT_CAPACITY = regulation.getRegulation('limitCapacity')
  SURCHARGE_CAPACITY = regulation.getRegulation('surchargeCapacity')
  SURCHARGE_FOREIGNER = regulation.getRegulation('surchargeForeigner')

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
  tax = 1
  isOverCapacity = False
  if(hasForeigner):
    tax=SURCHARGE_FOREIGNER.value
  elif(int(numberOfGuest) > LIMIT_CAPACITY.value):
    tax=SURCHARGE_CAPACITY.value
    isOverCapacity= True
  session['booking'] = {
    "tax": tax,
    "room": roomInfo.name,
    "roomId": roomInfo.id,
    "sex": currentUser.sex,
    "image": roomInfo.image,
    "description": roomInfo.description,
    "price": typeInfo.price,
    "arriveDate": arriveDate,
    "dayTotal": int(dayTotal),
    "email": currentUser.email,
    "hasForeigner": hasForeigner,
    "isOverCapacity": isOverCapacity,
    "address": currentUser.address,
    "numberOfGuest": numberOfGuest,
    "departureDate": departureDate,
    "lastname": currentUser.lastname,
    "firstname": currentUser.firstname,
    "isDone": False,
  }
  return session['booking']