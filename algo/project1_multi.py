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
from pagraph_model import pyltp_my
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

sentence = """
台湾工业总会是岛内最具影响力的工商团体之一，2008年以来，该团体连续12年发表对台当局政策的建言白皮书，集中反映岛内产业界的呼声。\
台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？\
围绕当局两岸政策，工总认为，由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地，建议台湾当局摒弃两岸对抗思维，在“求同存异”的现实基础上，以“合作”取代“对立”，为台湾多数民众谋福创利。\
工总现任理事长、同时也是台塑企业总裁的王文渊指出，过去几年，两岸关系紧张，不仅影响岛内观光、零售、饭店业及农渔蔬果产品的出口，也使得岛内外企业对投资台湾却步，2020年新任台湾领导人出炉后，应审慎思考两岸问题以及中国大陆市场。"""
import re

def token3(string):
    # we will learn the regular expression next course.
    string2=string.replace('\\n','') 
    return re.findall('\w+', string2) 

def get_head_parral_words(head, parse, words):
    re=[]
    for i in range(len(parse)):
      
        if parse[i][0]==head+1 and parse[i][1]=='COO':
            print("the parral head:is ",words[i] )
            re.append((i,words[i]))
    return re 
   
   #return -1,0
def get_genju(parse, words):  #根据。。报道
     if parse[0][1]=='ADV':
         for i in range(len(parse)):
            if parse[i][0]==1 and parse[i][1]=='POB':#and ('Ni'in NER[i] or 'Nh'in NER[i]):
                print('根据_head:',words[i] ) 
                return i,words[i] 
     return -1,0
def  VOB(head, parse, words):
    for i in range(len(parse)):
        if parse[i][0]==head+1 and parse[i][1]=='VOB':
            print("the VOB head:is ",words[i] )
            return i,words[i] 
    return -1,0

    
def  get_sub_words(head, parse, words):
    for i in range(len(parse)):
        if parse[i][0]==head+1 and parse[i][1]=='SBV':#and ('Ni'in NER[i] or 'Nh'in NER[i]):
            sub=i 
            print("主语是: ",words[i])
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

        # 找head
        for i in range(len(parse)):
            if parse[i][1]=='HED':
                head=i

        head_word=words[head]
        print("the origin head is ",head_word)


        if head!=0:  # eg：head=0"展望未来 (以动词开头的)
            if similar[head_word]>=2:
                sub_index,sub_word= get_sub_words(head, parse, words)
                result.append( sub_word)
                result.append( head_word)
                if words[head+1]=='，':

                    result.append(''.join(words[head+2:]))
                else:
                    result.append(''.join(words[head+1:]))
                #print(result)

        new_head,new_head_word=VOB(head, parse, words)  #工总现任理事长、同时也是。。。(eg,真正的核心和head是VOB)
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

        re=get_head_parral_words(head, parse, words)   #8月15日，中国联通举办年中业绩发布会 。。。 这种情况(eg,真正的核心和head是COO)
        if len(re)>0:
            for (parra_index,parral_word) in re:
                if   parral_word!=0:
                    if similar[parral_word]>=2:
                        sub_index,sub_word= get_sub_words( parra_index, parse, words)
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

        new_head,new_head_word=get_genju(parse, words)   #根据近期媒体报道，中国电信的5G...（e.g ：根据。。什么报道，类型）
        if  new_head_word!=0:
            if similar[new_head_word]>=2:
                sub_index,sub_word= get_sub_words(new_head, parse, words)
                result.append( sub_word)
                result.append( new_head_word)
                if words[new_head+1]=='，':

                    result.append(''.join(words[ new_head+2:]))
                else:
                    result.append(''.join(words[ new_head+1:]))
        results.append(result)
        if index>0:
            if len(results[index-1])>=1:
                if len(result)==0:
                    v1=X[(-1)*(length-index)].toarray()[0]
                    v2=X[(-1)*(length-index+1)].toarray()[0]
                    if distance(v1, v2)>=0.5:
                        results[index-1][-1]=results[index-1][-1]+sents[index]

    return result

if __name__ == '__main__':
    print(final_model(sentence))


