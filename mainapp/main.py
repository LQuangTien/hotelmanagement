from os import environ
from mainapp.model import room, reservation
from flask_mail import Message
from flask import render_template, session, jsonify
from mainapp import app, login, utils, mail
from flask_login import login_user, login_required
from mainapp.services import auth, room as roomService, reservation as reservationService

login.login_view = "login"

@login.user_loader
def userLoad(userId):
    return User.query.get(userId)


@app.route("/", methods=['post', 'get'])
def index():
    if request.method == 'GET':
        rooms = room.getAll()
        return render_template('hotel/index.html', error=request.args.get('error'), rooms=rooms)


@app.route("/history")
def history():
    page = request.args.get('page') or 1
    reservations, perPage, totalPage = reservationService.getAll()
    return render_template('hotel/history.html', reservations=reservations, perPage= perPage, totalPage=totalPage, page=int(page))


@app.route("/rooms")
def rooms():
    if request.method == 'GET':
        type, arriveDate, departureDate = roomService.handleGetRooms(request)
        rooms, perPage, totalPage = roomService.getByDate(type, arriveDate, departureDate)
        return render_template('hotel/our-room.html',
                               rooms=rooms, totalPage=totalPage, perPage=perPage)
@app.route("/our-rooms")
def ourRooms():
    if request.method == 'GET':
        rooms, perPage, totalPage = roomService.getAll()
        return render_template('hotel/our-room.html',rooms=rooms,visit=True, totalPage=totalPage, perPage=perPage)

@app.route("/aboutus")
@login_required
def aboutus():
    return render_template('hotel/about-us.html')


@app.route("/contact", methods=['post', 'get'])
def contact():
    if request.method == 'GET':
        return render_template('hotel/contact-us.html')
    if request.method == 'POST':
        name, email, message = auth.contactValidate(request)
        msg = Message("Customer's contact" ,
                      sender='tienkg5554@gmail.com',
                      recipients=['tienkg4445@gmail.com'])
        msg.body ="Email: " + email + "\n" + "Name: " + name + "\n" + message
        mail.send(msg)
        return redirect('/')


@app.route("/booking", methods=['post', 'get'])
@login_required
def booking():
    if request.method == 'GET':
        bookingInfo, qrURL, errorCode = roomService.handleGetBooking(request)
        return render_template('hotel/booking.html', bookingInfo=bookingInfo, qrURL=qrURL, errorCode=errorCode)
    if request.method == 'POST':
        bookingInfo, qrURL = roomService.handlePostBooking(request)
        return render_template('hotel/booking.html',bookingInfo=bookingInfo, qrURL=qrURL)


@app.errorhandler(404)
def notFound(e):
    return render_template('hotel/404.html'), 404


@app.route('/register', methods=['post', 'get'])
def register():
    if request.method == 'GET':
        return render_template('hotel/register.html')
    if request.method == 'POST':
        user, result = auth.registerValidate(request)
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
        user, error = auth.authValidate(request)
        if not user:
            return render_template('hotel/login.html', error=error)
        login_user(user=user)
        session['user'] = user.id
        next = utils.handleNextUrl(request)
        return redirect(next)


@app.route('/logout', methods=['post', 'get'])
def logout():
    if request.method == 'GET':
        logout_user()
        return redirect('/')

@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
    if request.method == 'POST':
        user,error = auth.authValidate(request)
        if user:
            login_user(user=user)
    return redirect('/admin')

@app.route('/api/roomtypes')
def roomtypes():
    types, maxCapacity = roomService.getRoomTypes()
    return jsonify({"types": types, "maxCapacity": maxCapacity})

if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True,port=int(environ.get('PORT')))