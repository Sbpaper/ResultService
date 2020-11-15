# coding: utf-8

from datetime import datetime
from app.Extensions import db
from flask_bcrypt import check_password_hash, generate_password_hash
import hashlib
from app.RAM import AppRAM
from app.Config import config
from sqlalchemy.dialects.mysql import LONGTEXT

class BaseModel(object):
    """模型基类，为每个模型补充创建时间与更新时间

    可以继承该基类给每个表加上create_time， update_time

    create_time:
            行创建时间

    update_time:
            每次该数据发送变化时会被更新

    """
    id = db.Column(db.Integer, primary_key=True)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(
        db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

    # def _get(self, id):
    #     """用id获取单条数据"""
    #     return self.query.filter_by(id=id).first()

    def _update(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '[ repr ] Class: %s, ID: %r' % (self.__class__.__name__, self.id)


class BaseModel_Account(object):
    """用户表模型基类

    为用户表和管理表继承相同字段和公共方法

    _set_token():
        设置token

    update():
        提交数据库
        self.commit()

    _clear_token():
        重置token
        account.self.token = None

    _is_correct_password(plaintext):
        检验密码 正确返回True 错误返回None

    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 记录的创建时间
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 记录的更新时间

    def _set_token(self):
        """设置新的Token"""
        from app.Tool import GenerateToken
        self.token = GenerateToken(str(self.email))
        db.session.commit()
        return True

    def _creater_password_hash(self, plaintext):
        newpassword = generate_password_hash(plaintext)
        self.password = newpassword

    def _set_new_password(self, plaintext):
        newpassword = generate_password_hash(plaintext)
        self.password = newpassword
        self._update()

    def _is_correct_password(self, plaintext):
        """判断密码 正确返回True"""
        if check_password_hash(self.password, plaintext):
            return True

    def _update(self):
        """提交至数据库"""
        db.session.add(self)
        db.session.commit()

    def _clear_token(self):
        """清除Token"""
        self.token = None
        db.session.commit()
        return True

    def __repr__(self):
        return '[ repr ] Class: %s, ID: %r' % (self.__class__.__name__, self.id)


class AccountAdmin(BaseModel_Account, db.Model):
    """管理员表"""

    __tablename__ = 'account_admin'
    account = db.Column(db.Text)
    username = db.Column(db.String(255))
    password = db.Column(db.Text)

    def toDict(self):
        return dict(
            id=self.id,
            token=self.token,
            account=self.account,
            username=self.username,
            password=self.password
        )

    def createadmin(self, username, account, password):
        self.account = account
        self.username = username
        self.password = generate_password_hash(password)
        self._update()
        return self


class AccountUser(BaseModel_Account, db.Model):
    """用户表"""

    __tablename__ = 'account_user'
    email = db.Column(db.Text)
    head = db.Column(db.Text)
    introduce = db.Column(db.Text)
    username = db.Column(db.String(255))
    password = db.Column(db.Text)
    status = db.Column(db.Integer, default=0)

    fans_count = db.Column(db.Integer, default=0)
    follow_count = db.Column(db.Integer, default=0)
    praised_count = db.Column(db.Integer, default=0) # 获赞

    # 空间字段
    space_introduce = db.Column(db.Text)
    space_url = db.Column(db.Text)
    space_bilibili = db.Column(db.Text)
    space_youtube = db.Column(db.Text)
    space_zhihu = db.Column(db.Text)
    space_github = db.Column(db.Text)

    def SetUserStatus(self, newstatus):
        """设置用户Status"""
        self.status = newstatus
        db.session.commit()

    @property
    def userhead(self):
        path = config[AppRAM.runConfig].STATIC_LOADPATH + '/static/head/'
        if self.head:
            return path + self.head
        return path + 'default-userhead.jpg'

    def toDict(self, type=[], userid=None):
        json = dict(
            id=self.id,
            head=self.userhead,
            introduce=self.introduce,
            username=self.username,
            fans_count=self.fans_count,
            follow_count=self.follow_count,
            praised_count=self.praised_count
        )

        if "space" in type:
            json = dict(json, **{
                "space_introduce": self.space_introduce,
                "space_url": self.space_url,
                "space_bilibili": self.space_bilibili,
                "space_youtube": self.space_youtube,
                "space_zhihu": self.space_zhihu,
                "space_github": self.space_github,
            })

        if "follow" in type:
            pass

        return json

class ArticleCategory(BaseModel, db.Model):
    __tablename__ = 'articlec_ategory'

    name = db.Column(db.String(255))
    weight = db.Column(db.Integer, default=0)

class ArticleActivity(BaseModel, db.Model):
    __tablename__ = 'articlea_ctivity'

    name = db.Column(db.String(255))
    weight = db.Column(db.Integer, default=0)
    pushstatus = db.Column(db.Boolean, default=False)   # 状态 False 不允许投稿 True 允许投稿
    startdate = db.Column(db.DateTime)
    overdate = db.Column(db.DateTime)

class ArticleData(BaseModel, db.Model):
    __tablename__ = 'article_data'

    title = db.Column(db.String(255))
    content = db.Column(LONGTEXT)
    introduce = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    sourceauthor = db.Column(db.String(255))        # 原作者
    sourceaddr = db.Column(db.Text)                 # 来源地址
    sourcetype = db.Column(db.Integer)              # 来源类型      1站内原创, 2趣味论文分享, 3趣味网文分享
    commentcount = db.Column(db.Integer, default=0) # 评论数统计
    uploaduser = db.Column(db.Integer)              # 上传的用户id
    is_delete = db.Column(db.Boolean, default=False)# 删除状态
    verify = db.Column(db.Integer)                  # 校验状态      0正常, 1未审核, 2被退回
    verifytxt = db.Column(db.Text)                  # 校验不合格说明
    Pageviews = db.Column(db.Integer, default=0)    # 浏览量
    maincategory = db.Column(db.Integer)            # 主类目
    activity = db.Column(db.Integer)                # 活动

    def toDict(self):
        return dict(
            title = self.title,
            content = self.content,
            introduce = self.introduce,
            cover = self.cover,
            sourceauthor = self.sourceauthor,
            sourceaddr = self.sourceaddr,
            sourcetype = self.sourcetype,
            commentcount = self.commentcount,
            uploaduser = self.uploaduser,
            is_delete = self.is_delete,
            verify = self.verify,
            verifytxt = self.verifytxt,
            create_time = datetime.strftime(self.create_time, "%Y-%m-%d %H:%M:%S"),
            update_time = datetime.strftime(self.update_time, "%Y-%m-%d %H:%M:%S")
        )

class FollowRecord(BaseModel, db.Model):
    __tablename__ = 'follow_record'

    userid = db.Column(db.Integer)
    follow_userid = db.Column(db.Integer)

class ThumbupRecord(BaseModel, db.Model):
    __tablename__ = 'thumbup_record'

    userid = db.Column(db.Integer)
    articleid = db.Column(db.Integer)

class Tag(BaseModel, db.Model):
    __tablename__ = 'tag'

    name = db.Column(db.String(255))

class TagBindRecord(BaseModel, db.Model):
    __tablename__ = 'Tag_bindrecord'

    tagid = db.Column(db.Integer)
    articleid = db.Column(db.Integer)

class TagSubRecord(BaseModel, db.Model):
    # sub(subscription)
    __tablename__ = 'tag_subrecord'

    tagid = db.Column(db.Integer)
    userid = db.Column(db.Integer)