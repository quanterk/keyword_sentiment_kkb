# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 12:21:45 2019

@author: K
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 15:24:45 2019

@author: K

"""
# 问题：1.model训练 （同义词准确性和全面性）出现的次数>=2. 2。后置语句 :通过引号确定位置 3.整篇文章：解决   
# import pandas as pd
# df = pd.read_csv('sqlResult_1558435.csv')
# print(df)

# file=open('sqlResult_1558435.csv','r',encoding='gb18030')
# news=file.readlines()
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cosine
from gensim.models import Word2Vec  
import pyltp_my
from collections import defaultdict
import jieba
import joblib
import os

def cut(string):
    return ' '.join(jieba.cut(string))

#model = Word2Vec.load("word2vec.model")
#model = Word2Vec.load("word2vec_final.model") 
#similar=get_related_words(['说','指出','报道','提出','表示','称'], model)   # 找说的近义词
path1 = os.path.dirname(os.path.abspath(__file__))
similar = joblib.load(path1 + '/keyword_similar.pkl')
'''
sentence = """
台湾工业总会是岛内最具影响力的工商团体之一，2008年以来，该团体连续12年发表对台当局政策的建言白皮书，集中反映岛内产业界的呼声。\
台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？\
围绕当局两岸政策，工总认为，由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地，建议台湾当局摒弃两岸对抗思维，在“求同存异”的现实基础上，以“合作”取代“对立”，为台湾多数民众谋福创利。\
工总现任理事长、同时也是台塑企业总裁的王文渊指出，过去几年，两岸关系紧张，不仅影响岛内观光、零售、饭店业及农渔蔬果产品的出口，也使得岛内外企业对投资台湾却步，2020年新任台湾领导人出炉后，应审慎思考两岸问题以及中国大陆市场。"""

sentence="""美国总统特朗普对福克斯新闻又不高兴了。在推特上，特朗普指责福克斯新闻“不再为我们工作”，说福克斯新闻干脆“向左转”算了。特朗普说，即使没有福克斯新闻的帮助，他也将赢得总统选举。
据美国哥伦比亚广播公司（CBS）8月28日报道，特朗普毫不掩饰他对福克斯新闻的2020年美国大选报道的不悦。特朗普此次被福克斯新闻“激怒”，是因为福克斯新闻主持人桑德拉·史密斯（Sandra Smith）对美国民主党全国委员会（DNC）通讯主任伊诺霍萨（Xochitl Hinojosa）的采访。特朗普在推特上批评桑德拉·史密斯对伊诺霍萨的言论毫无反驳，让伊诺霍萨“畅所欲言”，“大肆推销”民主党。
特朗普28日在推特上说：“我只想为人民赢得胜利。现在的福克斯新闻让数百万伟大的人失望了！我们必须要开始寻找一个新的新闻通讯社，福克斯新闻不再为我们工作了。” 美国有线电视新闻网（CNN）对此评论说，特朗普的这句话不经意间让人以为福克斯新闻像是一家国营电视台。即使从早上的“福克斯与朋友们”节目开始，福克斯新闻就有大量节目在为特朗普“助威”，特朗普依然觉得福克斯新闻不够忠诚。
据《洛杉矶时报》28日报道，福克斯新闻没有对特朗普发表在推特上的言论作出回应。但据CBS报道，福克斯新闻高级政治分析员布里特·休姆（Brit Hume）迅速在其个人推特上反驳特朗普，说“福克斯新闻不应该为你效劳”。休姆是一位资深保守派媒体人，曾在1989年至1996年担任美国广播公司（ABC）的白宫首席记者。
据报道，这只是特朗普近来在推特上对福克斯新闻批评的最新一项内容。在此前，特朗普还批评了福克斯新闻的其他评论员，如主持人胡安·威廉姆斯（Juan Williams）、克里斯·华莱士（Chris Wallace）与主播谢泼德·史密斯（Shepard Smith）等。
据CBS，威廉姆斯是福克斯新闻的政治分析员，他在《国会山》上刊文称，特朗普正在攻击的，是记者指出特朗普的谎言、批评他失败的政策以及督促他负责的能力。谢泼德·史密斯也是一位时常批评特朗普的新闻主播，特朗普曾批评说看他的新闻节目还不如去看他所厌恶的CNN。
据《洛杉矶时报》报道，经营保守派电视频道《新闻头条》（NewsMax）、身为特朗普朋友的克里斯托弗·拉迪（Christopher Ruddy）认为，特朗普对福克斯新闻的不满表明美国可以容纳不止一家保守派电视台。在一封电子邮件中，拉迪说美国人民和特朗普都厌倦了福克斯。
激起特朗普愤怒的民主党全国委员会通讯主任伊诺霍萨，则在微软全国广播公司（MSNBC）上回应称，她尊敬许多福克斯新闻的记者，她之所以参加福克斯节目是因为那里有重要的观众需要接触，她只希望特朗普在看福克斯新闻之外，做点更重要的事情。"""
'''
#sentence="特朗普在推特上批评桑德拉·史密斯对伊诺霍萨的言论毫无反驳，让伊诺霍萨“畅所欲言”，“大肆推销”民主党。"
sentence="""今年是中华人民共和国成立70周年，也是教师节设立35周年。日前，教育部表彰优秀教师。教师节，全国31个省份将为教师“亮灯”。北京1300余所大、中、小学以及370多条线路的公交车车载屏幕，将向教师“亮灯”致敬！
教育部教师工作司司长任友群介绍，目前，全国各级各类专任教师达1673.83万人，比1985年（931.9万人）增长79%；学历上，相比1985年，小学、初中取得本科及以上学历教师比例分别增加了61.59个百分点、80.59个百分点；能力上，2012年以来，“国培计划”培训各级各类教师超过1400万人次。教师地位待遇显著提升，教师工资由上世纪80年代之前在国民经济各行业排倒数后三位，提升到目前在全国19大行业排名第7位。
任友群透露，为了推进教师队伍建设，将加快出台新时代师德师风建设的意见，完善师德失范问题的防范与查处工作体系；还将做好中小学和幼儿园教师评价制度改革等措施。另外，教育部将协调部属师范大学，根据各地实际需求，增加公费师范生的供给。
教育部还将跟相关部委密切合作，通过跨部门、跨行业、跨地区调剂建立“周转池”等方式，增加中小学教师的编制，积极推动公办幼儿园编制标准的出台。
任友群表示，教育部将研制中小学教师岗位设置管理办法，优化学段岗位比例结构，指导地方落实职称评审向农村和边远地区倾斜的政策，推动教师职称评审和岗位设置相对均衡；在教师权益保障方面，教育部将研究改革和完善绩效工资总量核定办法，提高奖励性绩效工资比例，降低职称在绩效工资分配中的权重，单列班主任岗位津贴，推动提高教师教龄津贴标准。
今年教师节，教育部将表彰全国模范教师720名、全国教育系统先进工作者80名、全国教育系统先进集体600个，以及全国优秀教师1440名、全国优秀教育工作者160名。全国教书育人楷模推选活动也如期举办，今年将产生10位。
教育部教师工作司和中国教师发展基金会将继续发起“为教师亮灯”公益活动，号召全国各地地标建筑、交通设施、大中小学等在电子屏幕上滚动播放“老师您好”，目前，31个省份响应参加。北京1300多所大中小学，370余条线路上的公交车车载屏幕，将向教师“亮灯”致敬。"""

import re

def token3(string):
    # we will learn the regular expression next course.
    string2=string.replace('\\n','') 
    return re.findall('\w+', string2) 

def get_head_parral_words(head, parse, words):
    re=[]
    for i in range(len(parse)):
      
        if parse[i][0]==head+1 and parse[i][1]=='COO':
           # print("the parral head:is ",words[i] )
            re.append((i,words[i]))
    return re 
   
   #return -1,0
def get_genju(parse, words):  #根据。。报道
     if parse[0][1]=='ADV':
         for i in range(len(parse)):
            if parse[i][0]==1 and parse[i][1]=='POB':#and ('Ni'in NER[i] or 'Nh'in NER[i]):
               # print('根据_head:',words[i] ) 
                return i,words[i] 
     return -1,0
def  VOB(head, parse, words):
    for i in range(len(parse)):
        if parse[i][0]==head+1 and parse[i][1]=='VOB':
           # print("the VOB head:is ",words[i] )
            return i,words[i] 
    return -1,0

    
def  get_sub_words(head, parse, words):
    for i in range(len(parse)):
        if parse[i][0]==head+1 and parse[i][1]=='SBV':#and ('Ni'in NER[i] or 'Nh'in NER[i]):
            sub=i 
           # print("主语是: ",words[i])
            return i,words[i]
    
    return -1,0

#搜索代码
def get_related_words(initial_words, model):
    """
    @initial_words are initial words we already know
    @model is the word2vec model
    """
    
    unseen = initial_words
    
    seen = defaultdict(int)
    
    max_size = 1000  # could be greater
    
    while unseen and len(seen) < max_size:
        if len(seen) % 50 == 0: 
            print('seen length : {}'.format(len(seen)))
            
        node = unseen.pop(0)
        
        new_expanding = [w for w, s in model.most_similar(node, topn=20)]
        
        unseen += new_expanding
        
        seen[node] += 1
        
        # optimal: 1. score function could be revised
        # optimal: 2. using dymanic programming to reduce computing time
    
    return seen

def distance(v1, v2):
    return cosine(v1, v2)

def final_model(sentence):
    ltp = pyltp_my.HIT(sentence)
    sents=ltp.sentence_splitter()
    sents=[s for s in sents if len(s)>3]
    results=[]
    length=len(sents)
    pre_new= [token3(n) for n in sents]
    n2=[''.join(n) for n in pre_new]
    n3=[cut(n) for n in n2]
    # corpus=news+n3
    # vectorized = TfidfVectorizer(max_features=20)
    # X = vectorized.fit_transform(corpus)
    # joblib.dump(vectorized, 'tfidf_model.pkl')
    vectorized = joblib.load(path1 + '/tfidf_model.pkl')
    X = vectorized.transform(n3)

    for index,s in enumerate( sents):
        result=[]
        ltp2=pyltp_my.HIT(s)
        words=ltp2.segmentor()
        ltp2.posttagger()
        NER=ltp2.ner()
        parse=ltp2.parse()[1]  # 依存分析结果
        flag=True

        # 找head
        for i in range(len(parse)):
            if parse[i][1]=='HED':
                head=i

        head_word=words[head]
       # print("the origin head is ",head_word)


        if head!=0:  # eg：head=0"展望未来 (以动词开头的)
            if similar[head_word]>=2:
                sub_index,sub_word= get_sub_words(head, parse, words)
                if sub_word!=0:
                    result.append( sub_word)
                    result.append( head_word)
                    if words[head+1]=='，':  

                        result.append(''.join(words[ head+2:]))
                    else:
                        result.append(''.join(words[ head+1:]))
                    flag=False
        
                
                
                
                
                
                
                
                
                
        if flag:
            new_head,new_head_word=VOB(head, parse, words)  #工总现任理事长、同时也是。。。(eg,真正的核心和head是VOB)
            if   new_head_word!=0:
                if similar[new_head_word]>=2:
                    sub_index,sub_word= get_sub_words(new_head, parse, words)
                    if sub_word!=0:
                        result.append( sub_word)
                        result.append( new_head_word)
                        if words[new_head+1]=='，':
    
                            result.append(''.join(words[ new_head+2:]))
                        else:
                            result.append(''.join(words[ new_head+1:]))
                        flag=False
        if flag:                 
            re=get_head_parral_words(head, parse, words)   #8月15日，中国联通举办年中业绩发布会 。。。 这种情况(eg,真正的核心和head是COO)
            if len(re)>0:
                for (parra_index,parral_word) in re:
                    if   parral_word!=0:
                        if similar[parral_word]>=2:
                            sub_index,sub_word= get_sub_words( parra_index, parse, words)
                            if sub_word!=0:
                                result.append( sub_word)
                                result.append(parral_word)
                                if len(words)-parra_index<=3:
                                     begin=words.index("“")
                                     end=words.index("”")
                                     result.append(''.join(words[begin+1:end]))
                                elif words[ parra_index+1]=='，' or words[ parra_index+1]=='。':
                                    result.append(''.join(words[ parra_index+2:]))
                                else:
                                    result.append(''.join(words[ parra_index+1:]))
                                flag=False
        if flag:

            new_head,new_head_word=get_genju(parse, words)   #根据近期媒体报道，中国电信的5G...（e.g ：根据。。什么报道，类型）
            if  new_head_word!=0:
                if similar[new_head_word]>=2:
                    sub_index,sub_word= get_sub_words(new_head, parse, words)
                    if sub_word!=0:
                        result.append( sub_word)
                        result.append( new_head_word)
                        if words[new_head+1]=='，':
        
                            result.append(''.join(words[ new_head+2:]))
                        else:
                            result.append(''.join(words[ new_head+1:]))
                        flag=False
       
        results.append(result) 
    
        if index>0:
            if len(results[index-1])>=1:
                if len(result)==0:
                    v1=X[(-1)*(length-index)].toarray()[0]
                    v2=X[(-1)*(length-index+1)].toarray()[0]
                    if distance(v1, v2)>=0.5:
                        results[index-1][-1]=results[index-1][-1]+sents[index] 
    results=[result for result in results if result!=[]] 
                        
    return results

if __name__ == '__main__':
    
    print(final_model(sentence))


