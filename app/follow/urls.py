from app.follow import follow, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@follow.route('/user', methods=["POST"])
@TOKEN(2)
def FollowUser(request):
    """关注用户/取消关注
    Args:
        int     subid       被关注或取消关注的用户ID
    Returns:
        code    200 成功
                500 出错
        data    
            status
                1 关注成功
                0 取消关注成功
    """
    return ReturnRequest(views.FollowUser(request.json))

@follow.route('/list', methods=["POST"])
@NORMAL
def FollowFansList(request):
    """关注/粉丝列表
    Args:
        str     type         follow 关注列表, fans 粉丝列表
        int     userid       要获取的用户ID
        int     querypage    获取页数 默认是1
        int     perpage      分页返回数
    Returns:
    """
    return ReturnRequest(views.FollowList(request.json))