from app.Models import AccountUser, FollowRecord
from app.Tool import _Paginate

def FollowUser(request):
    current_account = request['current_account']

    subobj_id = request.get("subid",None)

    if not subobj_id:
        return 400, "参数有误", {}

    user = AccountUser.query.filter_by(id=subobj_id).first()
    if not user:
        return 400, ' 用户不存在', {}

    followrecord = FollowRecord.query.filter_by(userid = current_account.id, follow_userid=subobj_id).first()
    if not followrecord:

        # 未关注 执行关注

        try:

            # 被关注用户粉丝统计 + 1
            tofollowuser = AccountUser.query.get(subobj_id)
            tofollowuser.fans_count = int(tofollowuser.fans_count) + 1

            # 发起关注用户关注统计 + 1
            current_account.follow_count = int(current_account.follow_count) + 1

            # 添加关注记录
            addfollow = FollowRecord()
            addfollow.userid = current_account.id
            addfollow.follow_userid = tofollowuser.id
            db.session.add(addfollow)

            db.session.commit()

            return 200, "关注成功", {
                "status":1
            }

        except Exception as e:
            print(e)
            db.session.rollback()    # 发生异常时执行回滚
            return 500, "服务器傻逼了:错误码01", {}

    else:

        # 已经关注 执行取消关注

        try:

            # 被取消关注用户粉丝统计 - 1
            tofollowuser = AccountUser.query.get(subobj_id)
            tofollowuser.fans_count = int(tofollowuser.fans_count) - 1

            # 发起取消关注用户关注统计 - 1
            current_account.follow_count = int(current_account.follow_count) - 1

            # 删除关注记录
            db.session.delete(followrecord)
            db.session.commit()

            return 200, "取消关注成功", {
                "status":0
            }

        except Exception as e:
            print(e)
            db.session.rollback()    # 发生异常时执行回滚
            return 500, "服务器傻逼了:错误码02", {}

def FollowList(request):
    userid = request.get("userid",None)
    type = request.get('type',1)
    querypage = request.get('querypage',1)
    perpage = request.get('perpage',10)

    if not userid or type not in ["follow", "fans"]:
        return 400, "参数有误", {}

    if not AccountUser.query.get(userid):
        return 400, ' 用户不存在', {}

    if type == "follow":
        followbind = FollowRecord.query.filter_by(userid=userid).order_by(FollowRecord.create_time.desc())

    if type == "fans":
        followbind = FollowRecord.query.filter_by(follow_userid=userid).order_by(FollowRecord.create_time.desc())

    total, result, currentPage, totalPages = _Paginate(followbind, querypage, perpage)

    return 200, "", {
        "total":total,
        "result":[i.toDict() for i in result],
        "currentPage":currentPage,
        "totalPages":totalPages
    }