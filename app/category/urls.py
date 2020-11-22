from app.category import category, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@category.route('/querylist', methods=["POST"])
@NORMAL
def querylist(request):
    """获取分区列表"""
    return ReturnRequest(views.querylist(request.json))

@category.route('/categoryarticlelist', methods=["POST"])
@NORMAL
def CategoryArticleList(request):
    """分区文章列表"""
    return ReturnRequest(views.CategoryArticleList(request.json))

@category.route('/add', methods=["POST"])
@TOKEN(1)
def add(request):
    """新增分区"""
    return ReturnRequest(views.add(request.json))