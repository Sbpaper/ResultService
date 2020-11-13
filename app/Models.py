# coding: utf-8

from datetime import datetime
from app.Extensions import db
from flask_bcrypt import check_password_hash, generate_password_hash
import hashlib
from app.RAM import AppRAM
from app.Config import config

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