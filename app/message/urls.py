from app.message import message, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@message.route('/message', methods=["POST"])
@TOKEN(2)
def Demo_Api(request):
    """Demo"""
    return ReturnRequest(views.Demo_Api(request.json))