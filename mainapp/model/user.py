from mainapp.models import User


def get(id):
  return User.query.filter(User.id == id).first()