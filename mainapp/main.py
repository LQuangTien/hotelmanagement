from os import environ

from flask import render_template, request, redirect
from flask_login import login_user, login_required
from mainapp import app, login, utils, mail
from math import ceil
from mainapp.services.auth import authValidate, contactValidate, registerValidate
from flask_mail import Message
login.login_view = "login"


@login.user_loader
def userLoad(userId):
    return User.query.get(userId)


@app.route("/")
def index():
    return render_template('hotel/index.html')


@app.route("/rooms")
@login_required
def rooms():
    rooms = utils.getAll_room()
    perPage = 3
    totalPage = ceil(len(rooms)/perPage)
    return render_template('hotel/our-room.html',
                           rooms=rooms, totalPage=totalPage, perPage=perPage)


@app.route("/aboutus")
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


@app.route("/booking")
def booking():
    return render_template('hotel/room-booking.html')


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
        return redirect('/')

@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
    if request.method == 'POST':
        user = authValidate(request)
        if user:
            login_user(user=user)
    return redirect('/admin')


if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True,port=int(environ.get('PORT')))