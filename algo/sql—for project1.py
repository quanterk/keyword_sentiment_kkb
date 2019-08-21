# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 14:49:44 2019

@author: K
"""

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 

engine = create_engine('mysql+pymysql://root:AI@2019@ai@rm-8vbwj6507z6465505ro.mysql.zhangbei.rds.aliyuncs.com:3306/stu_db')
SessionClass=sessionmaker(bind=engine)
session=SessionClass()
from sqlalchemy.sql import text
s=text("SELECT content FROM news_chinese ") 
content=session.execute(s).fetchall() 

import re
def token3(string):
    # we will learn the regular expression next course.
    string2=string.replace('\\n','')
    
    return re.findall('\w+', string2) 
news=[token3(n[0]) for n in content]  
import jieba
def cut(string):
    return ' '.join(jieba.cut(string))
news2=[''.join(n) for n in news]
news3=[cut(n) for n in news2]  
with open('news_project1.txt','w',encoding='utf-8') as f:
    for n in news3:
        f.write(n+'\n')  