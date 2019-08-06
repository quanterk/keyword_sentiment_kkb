from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    '''
    浏览器输入 localhost:8080/hello/<您的名字>，即可出现问候语

    :param name: 用户姓名
    :return: Hello World web 模版
    '''
    return template('<b>Hello {{name}}</b>!', name=name)

run(host='localhost', port=8080)