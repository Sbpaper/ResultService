from app.Models import AccountUser

def Register(request):
    email = request.get('email', None)
    username = request.get('username', None)
    password = request.get('password', None)
    repassword = request.get('repassword', None)

    adduser = AccountUser()

    if password == repassword and email and username:
        adduser.email = email
        adduser.username = username
        adduser._creater_password_hash(password)
        adduser._update()

        return 200, "", {}
    
    return 400, "参数不正确", {}