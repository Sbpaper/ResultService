from app.Models import AccountUser

def UserInfo(request):
    print(request)
    id = request.get("id", None)
    if not id:
        return 400, "", {}

    obj = AccountUser.query.get(id)
    if not obj:
        return 400, "", {}

    return 200, "", obj.toDict(request['type'])

def ChangeInfo(request):
    print(request)

    current_account = request['current_account']
    # print(current_account)

    head = request.get("head", None)
    introduce = request.get("introduce", None)
    space_introduce = request.get("space_introduce", None)
    space_url = request.get("space_url", None)
    space_bilibili = request.get("space_bilibili", None)
    space_youtube = request.get("space_youtube", None)
    space_zhihu = request.get("space_zhihu", None)
    space_github = request.get("space_github", None)

    if head:
        current_account.head = head
    
    if introduce:
        current_account.introduce = introduce
    
    if space_introduce:
        current_account.space_introduce = space_introduce

    if space_url:
        current_account.space_url = space_url

    if space_bilibili:
        current_account.space_bilibili = space_bilibili

    if space_youtube:
        current_account.space_youtube = space_youtube

    if space_zhihu:
        current_account.space_zhihu = space_zhihu

    if space_github:
        current_account.space_github = space_github
    
    try:
        current_account._update()
        return 200, "", {
            "userhead": current_account.userhead
        }

    except Exception as e:
        print(e)
        return 400, "出错", {}

def ChangeUsername(request):
    print(request)

    current_account = request['current_account']

    username = request.get("username", None)

    if not username:
        return 400, "参数有误", {}

    current_account.username = username

    try:
        current_account._update()
        return 200, "", {}

    except Exception as e:
        print(e)
        return 400, "出错", {}

def ChangePassword(request):
    print(request)

    current_account = request['current_account']

    nowpassword = request.get("nowpassword", None)
    newpassword = request.get("newpassword", None)
    renewpassword = request.get("renewpassword", None)

    if newpassword != renewpassword:
        return 400, "两次密码不一致", {}

    if not current_account._is_correct_password(nowpassword):
        return 400, "当前密码不正确", {}

    current_account._set_new_password(newpassword)

    try:
        current_account._update()
        return 200, "", {}

    except Exception as e:
        print(e)
        return 400, "出错", {}

    