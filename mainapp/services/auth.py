import hashlib
from mainapp.models import User

def authValidate(request):
    username = request.form.get('username')
    password = request.form.get('password')
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()
    return user

def registerValidate(request):
    Username = request.form.get('Username')
    Password = request.form.get('Password')
    Email = request.form.get('Email')
    Lastname = request.form.get('Lastname')
    Firstname = request.form.get('Firstname')
    sex = request.form.get('sex')
    Address = request.form.get('Address')
    user = User(username=Username, password=Password, email=Email,
                firstname=Firstname, lastname=Lastname, address=Address, sex=sex, isActive=True,
                isAdmin=True)
    return user

def contactValidate(request):
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    return name, email, message