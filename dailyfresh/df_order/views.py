from django.shortcuts import render, redirect
from django.db import transaction
from datetime import datetime
from decimal import Decimal
from .models import OrderInfo, OrderDetailInfo
from df_user.islogin import islogin
from df_cart.models import CartInfo
from df_goods.models import GoodsInfo
from df_user.models import UserInfo
from django.http import JsonResponse


@islogin
def order(request):
    userid = request.session.get('user_id')
    user = UserInfo.objects.get(id=userid)

    # 接收cart.html的get请求
    orderid = request.GET.getlist('orderid')
    orderlist = []
    for id in orderid:
        orderlist.append(CartInfo.objects.get(id=int(id)))
    uphone = user.uphone[0:3] + '****' + \
        user.uphone[-4:] if user.uphone else ''

    context = {
        'page_name': True,
        'orderlist': orderlist,
        'user': user,
        'uphone': uphone,
    }

    return render(request, 'df_order/order.html', context)


'''
事务: 一旦操作失败则全部回退
1 创建订单对象
2 判断商品的库存
3 创建详单对象
4 修改商品库存
5 删除购物车
'''


# 装饰器: 事务保存点, 一旦有一步操作失败，则回滚全部操作
@transaction.atomic()
def order_handle(request):
    tran_id = transaction.savepoint()
    try:
        post = request.POST
        total = post.get('total')
        address = post.get('address')
        # 接收购物车id列表
        cart_ids = post.get('cart_ids')
        # 把u'1,3,5'先转成'utf-8'格式的字符串然后切分成[1,3,5]列表
        cart_ids = cart_ids.split(',')
        # print('cart_ids:', cart_ids)

        # 创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.ouser_id = uid
        order.odate = now.strftime('%Y %m %d %H:%M:%S')
        order.ototal = Decimal(total)
        order.oaddress = address
        order.save()

        # 遍历购物车中提交信息，创建订单详情表
        for cart_id in cart_ids:
            # 得到购物车对象
            cart = CartInfo.objects.get(id=int(cart_id))
            # 得到商品对象
            goods = cart.goods
            # 库存大于购买数量
            if goods.gstock >= cart.count:
                # 减少商品库存
                goods.gstock -= cart.count
                goods.save()
                # 创建订单详情对象
                detail = OrderDetailInfo()
                detail.order_id = order.oid
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # 提交订单后应该删除该购物车对象
                cart.delete()

            else:
                # 如果库存不够，触发事务回滚，撤销操作
                transaction.savepoint_rollback(tran_id)
                # 返回json给前台提示失败
                return JsonResponse({'status': 0})
        transaction.savepoint_commit(tran_id)
        # 返回json给前台提示成功

        return JsonResponse({'status': 1})
    except Exception as e:
        print('-'*20+('%s' % e))
        transaction.savepoint_rollback(tran_id)
        # # 返回json给前台提示成功
        return JsonResponse({'status': 2})



@transaction.atomic()
@islogin
def pay(request, orderid):
    tran_id = transaction.savepoint()
    try:

        order = OrderInfo.objects.get(oid=orderid)
        order.oIspay = 1
        order.save()
        transaction.savepoint_commit(tran_id)
        return JsonResponse({'status': 1})
    except Exception as e:
        print('-'*20+('%s' % e))
        transaction.savepoint_rollback(tran_id)
        return JsonResponse({'status': 0})


@islogin
def viewlog(request, orderid):
    return render(request, 'df_order/viewlog.html', context={'oid': int(orderid)})

