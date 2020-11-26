from flask import session

from mainapp.model import room


def bookingRoom(request):
  roomName = int(request.form.get("roomName"))
  roomInfo, typeInfo = room.get(roomName)
  #lấy thông tin user từ session của login
  #Từ thông tin đó query từ database gán vô session booking
  arriveDate = request.form.get("arriveDate")
  departureDate = request.form.get("departureDate")
  session['booking'] = {
    "room": roomInfo.name,
    "image": roomInfo.image,
    "price": typeInfo.price,
    "arriveDate": arriveDate,
    "departureDate": departureDate
  }
  return session['booking']