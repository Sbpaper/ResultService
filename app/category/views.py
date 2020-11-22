from app.Models import ArticleCategory, ArticleData
from app.Tool import _Paginate
from app.Extensions import db

def querylist(request):
    keyword = request.get('keyword',None)

    querys = ArticleCategory.query.filter()

    if keyword:
        querys = querys.filter(ArticleCategory.name.contains(keyword))

    querys = querys.order_by(ArticleCategory.create_time.desc())
    return 200, "", [i.toDict() for i in querys]


def CategoryArticleList(request):
    categoryid = request.get('categoryid',None)

    if not categoryid:
        return 400, "参数有误", {}

    querypage = request.get('querypage',1)  
    perpage = request.get('perpage',10)  

    querys = ArticleData.query.filter_by(categoryid=categoryid)
    querys = querys.order_by(ArticleData.create_time.desc())  

    total, result, currentPage, totalPages = _Paginate(querys, querypage, perpage)
    return 200, "", {
        "total":total,  
        "result":[i.toDict() for i in result],  
        "currentPage":currentPage,
        "totalPages":totalPages
    }

def add(request):
    name = request.get('name',None)
    if not name:
        return 400, "分区名不能为空", {}

    ArticleCategory().add(name)
    return 200, "成功", {}