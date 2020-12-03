from sqlalchemy import or_, func, not_

from mainapp import db
from mainapp.models import Regulation

def getRegulation(regulation):
  return Regulation.query.filter(Regulation.name == regulation).first()
