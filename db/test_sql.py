# 导入:
from sqlalchemy import Column, String, create_engine, VARCHAR
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()

# 定义User对象:
class Paragraph(Base):
    # 表的名字:
    __tablename__ = 'news_chinese'

    # 表的结构:
    id = Column(String(11), primary_key=True)
    author = Column(VARCHAR(length=32))
    content = Column(VARCHAR(length=1000))

# 初始化数据库连接:
host = 'rm-8vbwj6507z6465505ro.mysql.zhangbei.rds.aliyuncs.com'
root = 'root'
password = 'AI@2019@ai'
database = 'stu_db'

# mac_link = 'mysql+pymysql://<username>:<password>@<host>/<dbname>[?<options>]'
db_link = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(root, password, host, database)

engine = create_engine(db_link)

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
paragraph = session.query(Paragraph).filter(Paragraph.id=='5').one()
# 打印类型和对象的name属性:
print('type:', type(paragraph))
print('name:', paragraph.content)
# 关闭Session:
session.close()