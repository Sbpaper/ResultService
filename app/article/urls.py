from app.article import article, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@article.route('/demo-api', methods=["POST"])
@TOKEN(2)
def Demo_Api(request):
    """Demo"""
    return ReturnRequest(views.Demo_Api(request.json))