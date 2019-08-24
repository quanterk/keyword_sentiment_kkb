# -*- coding: utf-8 -*-
from pyltp  import SentenceSplitter
from pyltp import Segmentor
from pyltp import Postagger
from pyltp import NamedEntityRecognizer

text = "贵州财经大学要举办大数据比赛吗？那让欧几里得去问问看吧！其实是在贵阳花溪区吧。"
text = """
台湾工业总会是岛内最具影响力的工商团体之一，2008年以来，该团体连续12年发表对台当局政策的建言白皮书，集中反映岛内产业界的呼声。
台湾工业总会指出，2015年的白皮书就特别提到台湾面临“五缺”（缺水、缺电、缺工、缺地、缺人才）困境，使台湾整体投资环境走向崩坏。然而四年过去，“五缺”未见改善，反而劳动法规日益僵化、两岸关系陷入紧张、对外关系更加孤立。该团体质疑，台当局面对每年的建言，“到底听进去多少，又真正改善了几多”？
围绕当局两岸政策，工总认为，由数据来看，当前大陆不仅是台湾第一大出口市场，亦是第一大进口来源及首位对外投资地，建议台湾当局摒弃两岸对抗思维，在“求同存异”的现实基础上，以“合作”取代“对立”，为台湾多数民众谋福创利。
工总现任理事长、同时也是台塑企业总裁的王文渊指出，过去几年，两岸关系紧张，不仅影响岛内观光、零售、饭店业及农渔蔬果产品的出口，也使得岛内外企业对投资台湾却步，2020年新任台湾领导人出炉后，应审慎思考两岸问题以及中国大陆市场。
"""

#中文分词
segmentor = Segmentor()  #初始化实例
segmentor.load("/Users/ceil/PycharmProjects/personal/pyltp/ltp/ltp_data_model/cws.model")  #加载模型, 配绝对路径
words = segmentor.segment(text)  #分词
print(type(words))
print(' '.join(words))
segmentor.release()  #释放模型