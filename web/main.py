import sys
import os
file_dir = os.path.dirname(os.path.abspath('../'))
sys.path.append(file_dir)

from bottle import get, post, request, route, run, template, static_file
from algo.project1_multi import final_model

@get('/')
def index():
    return template('template/data_table.html')


# 获取数据
@post('/list')
def selectData():
    _result = request.POST.decode('utf-8')
    data = []
    result = {}
    username = _result.get('username').strip()
    # print(username)
    data1 = [1, "习近平", "指出", "既要决胜全面建成小康社会，又要开启全面建设社会主义现代化国家新征程"]
    data.append(data1)

    data2 = [2, "奥巴马", "提出", "两项不受布什现有教育政策框架限制,也不以特定利益团体为优惠对象的教育主张,即对学前教育提出“0岁至5岁教育计划”"]
    data.append(data2)

    data3 = [3, "马化腾", "认为", "发展产业互联网,将为实体经济高质量发展提供历史机遇和技术条件,提供新引擎和新动力,对实体经济产生全方位、深层次、革命性的影响"]
    data.append(data3)

    data4 = [4, "刘强东", "表示", "五环外的营收及活跃用户 截至2019年6月30日,京东过去12个月的活跃用户数为3.213亿,继续保持增长"]
    data.append(data4)

    if username is not None and username != "":
        user_result = [0] + final_model(username)
        # _data = []
        # for line in data:
        #     if username in line[1]:
        #         _data.append(line)
        result["data"] = [user_result]
    else:
        result["data"] = data
    result["code"] = 1
    return result


run(host="0.0.0.0", port=8868, server="tornado")
