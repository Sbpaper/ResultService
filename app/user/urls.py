from app.user import user, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@user.route('/info', methods=["POST"])
@NORMAL
def UserInfo(request):
    """获取用户信息
    Args:
        int     id      用户id
        arrny   type    返回包含那几种额外的数据    "space", "follow"

    Returns:
        id
        head
        introduce
        username
        fans_count
        follow_count
        praised_count

    space:
        space_introduce
        space_url
        space_bilibili
        space_youtube
        space_zhihu
        space_github
    """
    return ReturnRequest(views.UserInfo(request.json))

@user.route('/change/userinfo', methods=["POST"])
@TOKEN(2)
def ChangeInfo(request):
    """修改用户信息
    Args:
        head
        introduce
        space_introduce
        space_url
        space_bilibili
        space_youtube
        space_zhihu
        space_github

    Returns:
        code:
            200     成功
            400     失败
        data:
            userhead
    """
    return ReturnRequest(views.ChangeInfo(request.json))

@user.route('/change/username', methods=["POST"])
@TOKEN(2)
def ChangeUsername(request):
    """修改用户信息
    Args:
        str     username        用户名

    Returns:
        code:
            200     成功
            400     失败
        msg:
            业务消息

    """
    return ReturnRequest(views.ChangeUsername(request.json))

@user.route('/change/password', methods=["POST"])
@TOKEN(2)
def ChangePassword(request):
    """修改密码
    Args:
        str     nowpassword
        str     newpassword
        str     renewpassword

    Returns:
        code:
            200     成功
            400     失败
        msg:
            业务消息

    """
    return ReturnRequest(views.ChangePassword(request.json))