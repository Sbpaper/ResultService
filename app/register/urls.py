from app.register import register, views
from app.Common import ReturnRequest
from app.Middleware import NORMAL, TOKEN

@register.route('/register', methods=["POST"])
@NORMAL
def Register(request):
    """Demo"""
    return ReturnRequest(views.Register(request.json))