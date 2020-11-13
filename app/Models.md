建议:
    尽量不要用0做默认状态 处理不好会和None冲突

    规范说明:
    每个表必须存在更新时间和创建时间 可选参数[ index=True ] 设为索引
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    create_time = db.Column(db.DateTime, default=datetime.now)
    注: 建议直接继承基类 BaseModel

    基础Sql常用类型提供:
        参数说明[primary_key=True(设置字段内容不可重复), default(字段默认值)]
        db.Column(db.Integer, default=0)
        db.Column(db.Text)
        db.Column(db.String(255))
        db.Column(db.Date)
        db.Column(db.Boolean, default=False)
    
    常用参数序列化处理:
        datetime.strftime(self.字段名, "%Y-%m-%d %H:%M:%S")

    可选字段:
        软删除状态
        is_delete = db.Column(db.Boolean, default=False)

    toDict(self)使用方法:
        filter 默认下为空 '[]' 可以配合filter增加返回条件 如:

        1.
        filter = ['id']
        if "id" in filter:
        json = dict(json,**{"id": self.id})

        2.
        filter = ['userinfo']
        if "userinfo" in filter:
        json = dict(json,**{"userinfo": 用户表.query.filter_by(id=self.用户id).first().getUserinfo() })

    使用范文:
        def toDict(self, filter=[]):

            json = {
                'id': id,
            }
            return json

事务:
    flush: 写数据库，但不提交，也就是事务未结束
    commit: 是先调用flush写数据库，然后提交，结束事务，并开始新的事务
    flush之后你才能在这个Session中看到效果，而commit之后你才能从其它Session中看到效果
    db.session.add(mapping)
    db.session.flush()
    db.session.commit()

不采用
    class ErrorLog(BaseModel, db.Model):
        """用于储存程序发生的错误到数据库"""

        __tablename__ = 'error_log'
        address = db.Column(db.String(255))
        error_content = db.Column(db.Text)
        level = db.Column(db.Integer, default=0)

        def __init__(self, address, error_content, level=0):
            self.address = address
            self.error_content = error_content
            self.level = level
            self._update()

        def toDict(self):
            return dict(
                address = self.address,
                error_content = self.error_content,
                level = self.level
            )


    class DemoTable(BaseModel, db.Model):
        __tablename__ = 'demo_table'
        title = db.Column(db.String(255))
        content = db.Column(db.Text)

        def toDict(self):
            return dict(
                title=self.title,
                content=self.content
            )
