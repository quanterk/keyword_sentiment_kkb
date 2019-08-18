from bottle import get, post, request, route, run, template, static_file
import os

@get('/')
def index():
    currentPath = os.path.dirname(os.path.realpath(__file__)) # 获取当前路径
    print(currentPath)
    print('-------------------')
    print(template(currentPath + r'/main.tpl'))

@route('/bootstrap/dist/css/<filename>')
def server_static(filename):
    return static_file(filename, root='./bootstrap/dist/css/')

run(host='localhost', port=8081)