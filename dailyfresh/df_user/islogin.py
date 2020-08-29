#coding=utf-8
from django.http import HttpResponseRedirect

# 用作装饰器
#登录验证
def islogin(func):
    def login_fun(request,*args,**kwargs):
        # session中若存在登录信息,就继续执行func
        if request.session.get('user_id'):
            return func(request,*args,**kwargs)
        #如果没登录则转到登录页面
        else:
            red = HttpResponseRedirect('/user/login')
            # 将地址存入cookies,登录后跳转到来时想要查看的页面
            red.set_cookie('url',request.get_full_path())
            return red

    return login_fun

# http://127.0.0.1:8000/200/?type=10
# request.path: 表示当前路径, 为/200/
# reuqest.get_full_path: 表示完整路径, 为/200/?type=10