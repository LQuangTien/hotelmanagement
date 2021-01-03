import hashlib
from mainapp.models import User

def authValidate(request):
    username = request.form.get('username')
    isUsernameMatched = not not User.query.filter(User.username == username.strip()).first()

    if not isUsernameMatched:
        return None, "User not existed"

    password = request.form.get('password')
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    isPasswordMatched = not not User.query.filter(User.password == password).first()

    if not isPasswordMatched:
        return None, "Wrong password"

    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()
    return user, ""

def registerValidate(request):
    username = request.form.get('Username')
    password = request.form.get('Password')
    email = request.form.get('Email')
    lastname = request.form.get('Lastname')
    firstname = request.form.get('Firstname')
    sex = request.form.get('sex')
    address = request.form.get('Address')

    isUsernameDuplicate = not not User.query.filter(User.username == username.strip()).first()
    isMailDuplicate = not not User.query.filter(User.email == email.strip()).first()

    if isUsernameDuplicate:
        return None, "User existed"
    if isMailDuplicate:
        return None, "Email existed"

    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User(username=username, password=password, email=email,
                firstname=firstname, lastname=lastname, address=address,
                sex=sex, role=2)
    return user, "Register successfully"

def contactValidate(request):
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    return name, email, message