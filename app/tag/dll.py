from app.Models import Tag, TagBindRecord, TagSubRecord, TagIndex
from app.Extensions import db

def updateindex(tagid):
    obj = TagIndex.query.filter_by(tagid=tagid).first()
    if obj:
        obj.count = obj.count + 1
        obj._update()
    else:
        add = TagIndex()
        add.tagid = tagid
        add.count = 1
        add._update()

def create_tag_mapping(tagname):
    try:
        add_tag = Tag()
        add_tag.name = str(tagname)
        db.session.add(add_tag)
        db.session.flush()
        return add_tag
    except Exception as e:
        print(e)
        return None

def BindArticle(articleid, taglist = []):
    """DLL: 绑定文章TAG"""
    for i in taglist:
        a = Tag.query.filter_by(name=str(i)).first()
        if a:
            updateindex(a.id)
            if not TagBindRecord.query.filter_by(tagid=a.id, articleid=articleid).all():
                obj = TagBindRecord()
                obj.articleid = articleid
                obj.tagid = a.id
                db.session.add(obj)
                db.session.commit()
        else:
            addtype = create_tag_mapping(i)
            if addtype:
                updateindex(addtype.id)
                obj = TagBindRecord()
                obj.tagid = addtype.id
                obj.articleid = articleid
                db.session.add(obj)
                db.session.commit()