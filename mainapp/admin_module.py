from datetime import datetime

from flask import url_for, request
from flask_admin import BaseView, expose
from flask_login import logout_user, current_user
from werkzeug.utils import redirect

from mainapp import admin, db
from mainapp.models import User, Room, RoomType, Reservation, Regulation, Role
from flask_admin.contrib.sqla import ModelView

from mainapp.services import report
from mainapp.services.report import MyBarGraph


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 1

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_admin', next=request.url))


class CustomAuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == 1

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_admin', next=request.url))


class aboutUsView(CustomAuthenticatedView):
    @expose('/')
    def index(self):
        return self.render('admin/aboutus.html')



class ReportView(CustomAuthenticatedView):
    @expose('/')
    def index(self):
        args = request.args if request.args else None

        salesMonth = int(args.get('salesMonth')) if args else datetime.now().month
        salesYear = int(args.get('salesYear')) if args else datetime.now().year

        usedMonth = int(args.get('usedMonth')) if args else datetime.now().month
        usedYear = int(args.get('usedYear')) if args else datetime.now().year

        data, types = report.getReservationByQuery("total", salesMonth, salesYear)
        salesChart = MyBarGraph(data, types, "Biểu đồ tỉ lệ doanh thu theo từng loại phòng")
        salesChartJSON = salesChart.get()
        data2, types2 = report.getReservationByQuery("dayTotal", usedMonth, usedYear)
        usedChart = MyBarGraph(data2, types, "Biểu đồ tỉ lệ sử dụng theo từng loại phòng")
        usedChartJSON = usedChart.get()

        return self.render('admin/chart.html',
                           salesChartJSON=salesChartJSON, usedChartJSON=usedChartJSON,
                           salesMonth=salesMonth, salesYear=salesYear,
                           usedMonth=usedMonth, usedYear=usedYear)

class logoutView(CustomAuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        return self.render('admin/index.html')


class userView(AuthenticatedView):
    column_exclude_list = ['password', ]

admin.add_view(ReportView(name='Monthly Report'))
admin.add_view(userView(User, db.session))
admin.add_view(AuthenticatedView(Role, db.session))
admin.add_view(AuthenticatedView(Room, db.session))
admin.add_view(AuthenticatedView(RoomType, db.session))
admin.add_view(AuthenticatedView(Regulation, db.session))
admin.add_view(AuthenticatedView(Reservation, db.session))
admin.add_view(aboutUsView(name='About us'))
admin.add_view(logoutView(name='Logout'))

