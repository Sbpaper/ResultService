from app.tag import tag, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@tag.route('/item', methods=["POST"])
@NORMAL
def TagItem(request):
    """获取指定tag
    Args:
        int     id      tagid
    """
    return ReturnRequest(views.TagItem(request.json))

@tag.route('/list', methods=["POST"])
@NORMAL
def TagList(request):
    """TagList
    Args:
        int     querypage       分页            默认 1
        int     perpage         分页返回条数    默认 10
    """
    return ReturnRequest(views.TagList(request.json))

@tag.route('/tagvideolist', methods=["POST"])
@NORMAL
def TagVideoList(request):
    """获取指定tag的视频列表
    Args:
        int     id              tagid
        int     querypage       分页            默认 1
        int     perpage         分页返回条数    默认 10
    """
    return ReturnRequest(views.TagVideoList(request.json))

@tag.route('/sub', methods=["POST"])
@TOKEN(2)
def Sub(request):
    """关注TAG
    Args:
        int     tagid       被关注的标签
    """
    return ReturnRequest(views.Sub(request.json))

@tag.route('/search', methods=["POST"])
@NORMAL
def Search(request):
    """搜索TAG
    Args:
        int     keyword         搜索关键字
    """
    return ReturnRequest(views.Search(request.json))

@tag.route('/tophottaglist', methods=["POST"])
@NORMAL
def tophottaglist(request):
    """热门tag列表
    Args:
        int     keyword         搜索关键字
    """
    return ReturnRequest(views.tophottaglist(request.json))