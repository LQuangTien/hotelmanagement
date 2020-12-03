from sqlalchemy import or_, func, not_

from mainapp import db
from mainapp.models import Regulation

def getRegulation(regulation):
  return db.session.query(Regulation).filter(Regulation.name == regulation).first()
