import hashlib
from flask import render_template, request, redirect
from flask_login import login_user
from mainapp import app, login

@app.route("/")
def index():
    return render_template('hotel/index.html')
@app.route("/rooms")
def rooms():
    return render_template('hotel/our-room.html')
@app.route("/aboutus")
def aboutus():
    return render_template('hotel/about-us.html')
@app.route("/contact")
def contact():
    return render_template('hotel/contact-us.html')
@app.route("/gallery")
def gallery():
    return render_template('hotel/gallery.html')
@app.route("/booking")
def booking():
    return render_template('hotel/room-booking.html')
@app.route("/404")
def notFound():
    return render_template('hotel/404.html')

@login.user_loader
def userLoad(userId):
    return User.query.get(userId)


@app.route('/login-admin', methods=['post', 'get'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        print(user)
        if user:
            login_user(user=user)

    return redirect('/admin')


if __name__ == "__main__":
    from mainapp.admin_module import *
    app.run(debug=True,port=8900)