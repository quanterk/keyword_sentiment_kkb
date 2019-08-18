from bottle import get, post, request, route, run, template, static_file
import os

@get('/mainlinkmode')
def iframe_form():
    currentPath=os.path.dirname(os.path.realpath(__file__)) #获取当前路径
    return template(currentPath+r'\mainlink.tpl')

run(host='localhost', port=8081)