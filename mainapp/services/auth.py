import hashlib
from mainapp.models import User

def authValidate(request):
    username = request.form.get('username')
    password = request.form.get('password')
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    user = User.query.filter(User.username == username.strip(),
                             User.password == password).first()
    return user

def contactValidate(request):
    name = request.form.get('name')
    mail = request.form.get('email')
    message = request.form.get('message')
    return name, mail, message