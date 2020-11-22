from app.login import login, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@login.route('/signin', methods=["POST"])
@NORMAL
def Signin(request):
    """登录接口"""
    return ReturnRequest(views.Signin(request.json))

@login.route('/admin', methods=["POST"])
@NORMAL
def adminlogin(request):
    """管理员登录接口"""
    return ReturnRequest(views.adminlogin(request.json))