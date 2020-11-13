from app.user import user, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@user.route('/info', methods=["POST"])
@NORMAL
def UserInfo(request):
    """获取用户信息"""
    return ReturnRequest(views.UserInfo(request.json))

@user.route('/changeinfo', methods=["POST"])
@TOKEN(2)
def ChangeInfo(request):
    """获取用户信息"""
    return ReturnRequest(views.ChangeInfo(request.json))