from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse, JsonResponse
from .models import UserInfo
from df_goods.models import GoodsInfo
from df_order.models import OrderInfo
from hashlib import sha1
from .islogin import islogin
from django.core.paginator import Paginator


# 注册页面
def register(request):
    context = {'title': '用户注册'}
    return render(request, 'df_user/register.html', context)


# 注册处理
def register_handle(request):
    # 接收用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')
    # 判断两次密码
    if upwd != ucpwd:
        # 重定向
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upwd3 = s1.hexdigest()
    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    # 注册成功,转到登录页面
    return redirect('/user/login/')


# 判断用户是否已经存在
def register_exist(requset):
    uname = requset.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


# 登录界面
def login(request):
    uname = request.COOKIES.get('uname', '')  # 尝试读取cookies缓存的用户消息,没有就返回''
    context = {'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


# 这里使用的是Request对象方法
# 推荐使用框架的ajax相关方法，不要使用XMLHttpRequest对象，因为操作麻烦且不容易查错
# 登录处理
def login_handle(request):
    # 接收请求信息
    get = request.POST
    uname = get.get('username')
    upwd = get.get('pwd')
    jizhu = get.get('jizhu', '0')  # 1记住,0不记住,若没有读到值,则,使jizhu为默认值0
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)  # 如果用get()没查到会异常，fiter则是返回空列表

    # print uname
    # 等于1：从数据库中查询到用户，接下来判断密码是否正确即可
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd.encode('utf-8'))

        # 登录带cookie值   必须 red = HttpResponseRedirect    red.set_cookie  renturn red

        # 用户名正确，判断输入的密码是否正确
        # 相等：密码正确
        if s1.hexdigest() == users[0].upwd:

            # 登陆成功,从cookies中读取来时的地址,从哪来回哪去
            # 若cookies没有该数据,默认跳转到首页
            url = request.COOKIES.get('url', '/')
            red = HttpResponseRedirect(url)
            # 删除cookie
            red.delete_cookie('url')

            # count = CartInfo.objects.filter(user_id=users[0].id).count()
            # print '*'*10
            # print count

            # 是否勾选记住用户名
            # 勾选记住用户名
            if jizhu == '1':
                # 设置cookie
                red.set_cookie('uname', uname)
            # 不勾选记住用户名
            else:
                # -1：cookie马上过期
                red.set_cookie('uname', '', max_age=-1)
                # 删除cookie
                # red.set_cookie('url')

            # 存储信息到session中，方便其他页面使用
            # 比如:当在首页点击购物车,检查该数据存在与否可判断用户是否登录,没登录让用户登录
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            # request.session['count'] = count

            return red

        # 不相等：密码错误，显示提示消息
        else:
            context = {'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)

    # 不等于1：数据库中不存在用户，说明用户名错误，显示提示消息
    else:
        context = {'error_name': 1, 'error_pwd': 0, 'uname': uname}
        return render(request, 'df_user/login.html', context)


# 登录用户中心
@islogin
def info(request):
    # 根据用户id去查邮箱
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail

    # 最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_id_list = goods_ids.split(',')
    goods_list = []
    # print(goods_id_list)
    if len(goods_ids):
        for goods_id in goods_id_list:
            goods_list.append(GoodsInfo.objects.get(id=int(goods_id)))

    context = {'user_email': user_email,
               'user_name': request.session['user_name'],
               'page_name': True,
               # 'guest_cart': True,
               # 'info':1,
               'goods_list': goods_list
               }

    return render(request, 'df_user/user_center_info.html', context)


# 收货地址
# 这个视图既能接收post请求也能接收get请求
# post请求：地址信息修改后
# get请求：显示
@islogin
def site(request):
    # 根据id去查user
    user = UserInfo.objects.get(id=request.session['user_id'])

    # 接收修改后的地址信息
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uphone = post.get('uphone')
        user.uyoubian = post.get('uyoubian')
        user.save()

    context = {'user': user, 'page_name': True, 'site': 1}
    return render(request, 'df_user/user_center_site.html', context)


# 登出
def logout(request):
    # 清楚所有session
    request.session.flush()
    return redirect('/')


# 订单
@islogin
def order(request, pageindex):
    userid = request.session['user_id']
    orders = OrderInfo.objects.filter(ouser_id=userid)

    paginator = Paginator(orders, 2)
    page = paginator.page(int(pageindex))
    pagelist = paginator.page_range

    context = {'page_name': True,
               'page':page,
               'pagelist': pagelist,
               }
    return render(request, 'df_user/user_center_order.html', context)
