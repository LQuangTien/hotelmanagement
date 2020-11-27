from os import environ

import flask
from flask import render_template, request, redirect, session
from flask_login import login_user, login_required
from mainapp import app, login, utils, mail
from math import ceil

from mainapp.model import room
from mainapp.services.auth import authValidate, contactValidate, registerValidate
from flask_mail import Message

from mainapp.services.room import bookingRoom
from mainapp.utils import handleNextUrl

login.login_view = "login"

@login.user_loader
def userLoad(userId):
    return User.query.get(userId)


@app.route("/")
def index():
    return render_template('hotel/index.html', error=request.args.get('error'))


@app.route("/rooms")
def rooms():
    if request.method == 'GET':
        type = None if request.args.get('type') == 'Any' else request.args.get('type')
        arriveDate = request.args.get('arriveDate')
        departureDate = request.args.get('departureDate')
        rooms = room.getByQuery(type, arriveDate, departureDate)
        perPage = 3
        totalPage = ceil(len(rooms)/perPage)
        numberOfGuest = int(request.args.get("numberOfGuest"))
        hasForeigner = request.args.get("hasForeigner")
        hasForeigner = True if hasForeigner == 'True' else False
        session['bookForm'] = {
            "arriveDate": arriveDate,
            "departureDate": departureDate,
            "numberOfGuest": numberOfGuest,
            "hasForeigner": hasForeigner,
            "type": type
        }
        return render_template('hotel/our-room.html',
                               rooms=rooms, totalPage=totalPage, perPage=perPage,
                               arriveDate=arriveDate, departureDate=departureDate)


@app.route("/aboutus")
@login_required
def aboutus():
    return render_template('hotel/about-us.html')




@app.route("/contact", methods=['post', 'get'])
def contact():
    if request.method == 'GET':
        return render_template('hotel/contact-us.html')
    if request.method == 'POST':
        name, email, message = contactValidate(request)
        msg = Message('Hello',
                      sender='tienkg5554@gmail.com',
                      recipients=['tienkg4445@gmail.com'])
        msg.body = email + "\n" + name + "\n" + message
        mail.send(msg)
        return redirect('/')


@app.route("/gallery")
def gallery():
    return render_template('hotel/gallery.html')


@app.route("/booking", methods=['post', 'get'])
@login_required
def booking():
    if request.method == 'GET':
        return render_template('hotel/booking.html')
    if request.method == 'POST':
        bookingInfo = bookingRoom(request)
        return render_template('hotel/booking.html',bookingInfo=bookingInfo)


@app.errorhandler(404)
def notFound(e):
    return render_template('hotel/404.html'), 404


@app.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'GET':
        return render_template('hotel/register.html')
    if request.method == 'POST':
        user, result = registerValidate(request)
        if not user:
            return render_template('hotel/register.html', error=result)
        db.session.add(user)
        db.session.commit()
        return render_template('hotel/register.html', result=result)


@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'GET':
        return render_template('hotel/login.html')
    if request.method == 'POST':
        user, error = authValidate(request)
        if not user:
            return render_template('hotel/login.html', error=error)
        login_user(user=user)
        session['user'] = user.id
        next = handleNextUrl(request)
        return redirect(next)

@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
    if request.method == 'POST':
        user,error = authValidate(request)
        if user:
            login_user(user=user)
    return redirect('/admin')


if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True,port=int(environ.get('PORT')))