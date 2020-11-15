from app.Models import ArticleData
from app.Tool import _Paginate

def Get(request):
    id = request.get("id",None)
    if not id:
        return 400, "参数有误", {}
    article = ArticleData.query.get(id)
    return 200, "", article.toDict()

def Query(request):
    maincategory = request.get("maincategory", None)
    sourcetype = request.get("sourcetype", None)
    querypage = request.get('querypage',1)
    sort = request.get('sort',"new")
    perpage = request.get('perpage',10)
    userid = request.get('userid',None)

    querys = ArticleData.query.filter(ArticleData.is_delete==False,ArticleData.verify==0)
    
    if userid:
        querys = querys.filter(ArticleData.uploaduser == userid)

    if sourcetype:
        querys = querys.filter(ArticleData.sourcetype == sourcetype)

    if sort == "tohot":
        querys = querys.order_by(ArticleData.Pageviews.desc())

    if sort == "topnew":
        querys = querys.order_by(ArticleData.create_time.desc())

    if sort == "topcomment":
        querys = querys.order_by(ArticleData.commentcount.desc())

    total, result, currentPage, totalPages = _Paginate(querys, querypage, perpage)

    return 200, "", {
        "total":total,  
        "result":[i.toDict() for i in result],  
        "currentPage":currentPage,  
        "totalPages":totalPages
    }