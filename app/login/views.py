from app.Models import AccountUser

def Signin(request):
    account = request.get("account",None)
    password = request.get("password",None)

    obj = AccountUser.query.filter(AccountUser.email == account).first()
    if obj and obj._is_correct_password(password):
        obj._set_token()
        return 200, "", {
            "token": obj.token,
            "username": obj.username,
            "head": obj.userhead,
            "id": obj.id,
        }
        
    return 400, "账户密码不正确", {}