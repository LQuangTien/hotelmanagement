from mainapp.models import RoomType


def getAll():
  return RoomType.query.all()