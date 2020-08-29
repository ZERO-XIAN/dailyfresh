from django.shortcuts import render, redirect
from django.http import JsonResponse
from df_user.islogin import islogin
from django.db.models import Sum
from .models import*


def get_cartcount(request):
    # 购物车数量
    userid = request.session.get('user_id')
    cartcount = CartInfo.objects.filter(user_id=userid).aggregate(Sum('count'))['count__sum']
    request.session['cartcount'] = cartcount
    return cartcount


@islogin
def cart(request):
    userid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=userid)
    # lenn = len(carts)
    context = {
        'title': '购物车',
        'page_name': 1,
        'carts': carts,
        # 'len':lenn,
    }
    return render(request, 'df_cart/cart.html', context)


@islogin
def add(request, goodsid, count):
    userid = request.session['user_id']
    carts = CartInfo.objects.filter(user_id=userid, goods_id=goodsid)
    if len(carts) >= 1:
        cart = carts[0]
        # print(cart)
        cart.count = cart.count + count
    else:
        cart = CartInfo()
        cart.user_id = userid
        cart.goods_id = goodsid
        cart.count = count
    cart.save()
    # 购物车中商品的总数(同样的商品只算1个)
    # cartcount = CartInfo.objects.filter(user_id=userid).count()

    # 聚合函数-求和-购物车中商品的数量(同样的商品的数量有多少算多少)
    # cartcount = CartInfo.objects.filter(user_id=userid).aggregate(Sum('count'))['count__sum']
    # request.session['cartcount'] = cartcount
    cartcount = get_cartcount(request)

    # 如果是ajax请求则返回json,否则转向购物车
    if request.is_ajax():
        return JsonResponse({'cartcount': cartcount})
    else:
        return redirect('/cart/')


@islogin
def delete(request, cartid):
    try:
        cart = CartInfo.objects.get(pk=int(cartid))
        cart.delete()
        userid = request.session['user_id']
        cartcount = get_cartcount(request)

        data = {'ok': 1, 'cartcount': cartcount}
    except:
        data = {'ok': 0, }
    return JsonResponse(data)


@islogin
def edit(request, cartid, count):
    try:
        cart = CartInfo.objects.get(pk=int(cartid))
        cart.count = count
        cart.save()
        data = {'ok': 0}
        get_cartcount(request)

    except:
        data = {'ok': count}

    return JsonResponse(data)
