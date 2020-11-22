from app.article import article, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@article.route('/get', methods=["POST"])
@NORMAL
def Get(request):
    """获取单篇文章"""
    return ReturnRequest(views.Get(request.json))


@article.route('/query', methods=["POST"])
@NORMAL
def Query(request):
    """获取文章列表"""
    return ReturnRequest(views.Query(request.json))

@article.route('/admin/articlelist', methods=["POST"])
@TOKEN(1)
def AdminArticleList(request):
    """管理员用获取接口"""
    return ReturnRequest(views.AdminArticleList(request.json))

@article.route('/push', methods=["POST"])
@TOKEN(2)
def Psuh(request):
    """发布文章"""
    return ReturnRequest(views.Push(request.json))