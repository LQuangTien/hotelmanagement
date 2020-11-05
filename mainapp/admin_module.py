from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from mainapp import admin, db
from mainapp.models import User, Room
from flask_admin.contrib.sqla import ModelView

class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class CustomAuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated

class aboutUsView(CustomAuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/aboutus.html')


class logoutView(CustomAuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return self.render('admin/index.html')


admin.add_view(AuthenticatedView(User, db.session))
admin.add_view(AuthenticatedView(Room, db.session))
admin.add_view(aboutUsView(name='About us'))
admin.add_view(logoutView(name='Logout'))

