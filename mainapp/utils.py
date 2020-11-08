from mainapp.models import Room

def getAll_room():
    return Room.query.all()