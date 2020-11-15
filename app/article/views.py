from app.Models import ArticleData, ArticleCategory, ArticleActivity
from app.Tool import _Paginate
from datetime import datetime

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

def Push(request):
    id = request.get("id",None)

    title = request.get("title",None)
    content = request.get("content",None)
    introduce = request.get("introduce",None)
    cover = request.get("cover",None)
    sourceauthor = request.get("sourceauthor",None)
    sourceaddr = request.get("sourceaddr",None)
    sourcetype = request.get("sourcetype",None)
    maincategory = request.get("maincategory",None)
    activity = request.get("activity",None)

    if sourcetype in [2,3]:
        if not sourceauthor:
            return 400, "原作者不能为空", {}

    if not title:
        return 400, "标题不能为空", {}

    if not content:
        return 400, "内容不能为空", {}

    if not introduce:
        return 400, "介绍不能为空", {}

    if not cover:
        return 400, "封面不能为空", {}

    requesttype = None

    # 创建对象
    if id:
        articleobj = ArticleData.query.get(id)
        if not articleobj:
            return 400, "文章不存在", {}
        requesttype = "edit"
    else:
        articleobj = ArticleData()
        requesttype = "create"

    categoryobj = ArticleCategory.query.get(maincategory)
    if not categoryobj:
        return 400, "分区有误", {}
    else:
        articleobj.maincategory = categoryobj

    if activity:
        activityobj = ArticleActivity.query.get(activity)
        if not activityobj:
            return 400, "活动不存在", {}

        if activityobj.overdate >= datetime.now():
            return 400, "该活动已结束", {}

        if activityobj.pushstatus == False:
            return 400, "该活动已不允许投稿", {}

        if requesttype == "create":
            articleobj.activity = activity

    articleobj.title = title
    articleobj.content = str(content)
    articleobj.introduce = introduce
    articleobj.cover = cover
    articleobj.sourceauthor = sourceauthor
    articleobj.sourceaddr = sourceaddr
    articleobj.sourcetype = sourcetype
    articleobj.maincategory = maincategory
    articleobj._update()
    return 200, "", articleobj.id