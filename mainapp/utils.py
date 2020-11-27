from datetime import datetime
from functools import wraps

from flask import session, url_for, redirect, request
from flask_login import current_user


def subtractDate(firstDateString, seccondDateString):
  result = datetime.strptime(firstDateString, '%Y-%m-%d') - datetime.strptime(seccondDateString, '%Y-%m-%d')
  return result.total_seconds()

def handleNextUrl(request):
  if not request:
    return None
  next = request.args.get('next')
  if next == None:
    return '/'
  bookForm = session.get('bookForm')
  if bookForm:
    return f"rooms?arriveDate={bookForm['arriveDate']}&departureDate={bookForm['departureDate']}&type={bookForm['type']}&numberOfGuest={bookForm['numberOfGuest']}&hasForeigner={bookForm['hasForeigner']}"
  return next