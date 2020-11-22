from app.Models import Tag, TagBindRecord, TagSubRecord, TagIndex, ArticleData
from app.Tool import _Paginate
from app.Extensions import db
from datetime import datetime, timedelta

def TagItem(request):
    tagid = request.get('tagid',None)

    if not tagid:
        return 400, "ID不能为空", {}

    return 200, "", Tag.query.get(tagid).toDict()

def TagVideoList(request):
    tagid = request.get('tagid',None)
    querypage = request.get('querypage',1)  
    perpage = request.get('perpage',10)  

    idlist = TagBindRecord.query.filter_by(tagid=tagid).order_by(Tag.create_time.desc())
    total, result, currentPage, totalPages = _Paginate(idlist, querypage, perpage)  
    
    result = [ ArticleData.query.get(i.articleid).toDict() for i in result]

    return 200, "", {  
        "total":total,  
        "result":result,  
        "currentPage":currentPage,  
        "totalPages":totalPages
    }

def TagList(request):
    querypage = request.get('querypage',1)  
    perpage = request.get('perpage',10)  

    querys = Tag.query.filter()  
    querys = querys.order_by(Tag.create_time.desc())

    total, result, currentPage, totalPages = _Paginate(querys, querypage, perpage)  
    return 200, "", {  
        "total":total,  
        "result":[i.toDict() for i in result],  
        "currentPage":currentPage,  
        "totalPages":totalPages
    }


def Sub(request):
    current_account = request['current_account']
    tagid = request.get('tagid',None)
    
    record = TagSubRecord.query.filter_by(userid=current_account.id, tagid=tagid).first()

    if not record:
        TagSubRecord().addSub(tagid, current_account.id)
        return 200, "订阅成功", dict(status=1)
    else:
        db.session.delete(record)
        db.session.commit()
        return 200, "取消订阅成功", dict(status=0)


def Search(request):
    keyword = request.get('keyword',None)

    if not keyword:
        return 400, "搜索关键字不能为空", {}

    querys = Tag.query.filter(Tag.name.contains(keyword)).all()

    return 200, "", [{"value":i.toDict()["name"]} for i in querys]


def tophottaglist(request):
    NOW = datetime.now()
    querys = TagIndex.query.filter(TagIndex.update_time >= NOW - timedelta(days=7)).order_by(TagIndex.count.desc()).limit(8)
    a = []
    for i in querys:
        if i.tagid:
            obj = Tag.query.get(i.tagid)
            if obj:
                a.append(obj.toDict())
    return 200, "", a