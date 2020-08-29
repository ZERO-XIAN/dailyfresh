from .models import GoodsInfo, TypeInfo
from django.shortcuts import render
from django.core.paginator import Paginator, Page
from df_cart.models import CartInfo
from django.db.models import Sum
from haystack.views import SearchView


def get_cartcount(request):
    # 购物车数量
    userid = request.session.get('user_id')
    cartcount = CartInfo.objects.filter(user_id=userid).aggregate(Sum('count'))['count__sum']
    request.session['cartcount'] = cartcount
    return cartcount

# Create your views here.
# 查询每类商品最新的4个和点击率最高的4个
def index(request):
    get_cartcount(request)

    #主页
    typelist = TypeInfo.objects.all()
    type0 = typelist[0].goodsinfo_set.order_by("-id")[:4]
    type01 = typelist[0].goodsinfo_set.order_by("-gclick")[:4]
    type1 = typelist[1].goodsinfo_set.order_by("-id")[:4]
    type11 = typelist[1].goodsinfo_set.order_by("-gclick")[:4]
    type2 = typelist[2].goodsinfo_set.order_by("-id")[:4]
    type21 = typelist[2].goodsinfo_set.order_by("-gclick")[:4]
    type3 = typelist[3].goodsinfo_set.order_by("-id")[:4]
    type31 = typelist[3].goodsinfo_set.order_by("-gclick")[:4]
    type4 = typelist[4].goodsinfo_set.order_by("-id")[:4]
    type41 = typelist[4].goodsinfo_set.order_by("-gclick")[:4]
    type5 = typelist[5].goodsinfo_set.order_by("-id")[:4]
    type51 = typelist[5].goodsinfo_set.order_by("-gclick")[:4]

    # # 构造上下文
    context = {'title': '首页', 'guest_cart': True,
               'type0': type0, 'type01': type01,
               'type1': type1, 'type11': type11,
               'type2': type2, 'type21': type21,
               'type3': type3, 'type31': type31,
               'type4': type4, 'type41': type41,
               'type5': type5, 'type51': type51, }
    # 返回渲染模板
    return render(request, 'df_goods/index.html', context)


# 商品列表
def goodlist(request, typeid, pageindex, sort):

    # count = request.session.get('count')

    # 根据商品分类获取实际商品信息
    typeinfo = TypeInfo.objects.get(pk=typeid)
    # 获取最新发布的商品
    newgoods = typeinfo.goodsinfo_set.order_by('-id')[:2]
    # 根据条件查询所有商品
    if sort == 1:  # 按最新   gtype_id  , gtype__id  指typeinfo_id
        good_list = GoodsInfo.objects.filter(gtype_id=typeid).order_by('-id')
    elif sort == 2:  # 按价格
        good_list = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('gprice')
    elif sort == 3:  # 按点击量
        good_list = GoodsInfo.objects.filter(
            gtype__id=typeid).order_by('-gclick')

    # 分页:将排序好的商品分页
    paginator = Paginator(good_list, 10)
    # 每页对应的商品
    page_goods = paginator.page(pageindex)
    # 页码列表
    page_list = paginator.page_range

    # 构造上下文  'count': count,
    context = {
        'goodstype': typeinfo.ttitle,
        'guest_cart': True,
        'page_goods': page_goods,
        'page_list': page_list,
        'typeid': typeid,
        'pageindex': pageindex,
        'sort': sort,
        'newgoods': newgoods,
    }

    # 渲染返回结果
    return render(request, 'df_goods/list.html', context)


# 商品详细信息
def detail(request, goodsid):
    goods = GoodsInfo.objects.get(pk=goodsid)
    # 点击量
    goods.gclick += 1
    goods.save()
    newgoods = goods.gtype.goodsinfo_set.order_by('-id')[0:2]
    context = {
        'goodstype': goods.gtype,
        'guest_cart': True,
        'goods': goods,
        'newgoods': newgoods,
    }

    # return render(request,'df_goods/detail.html',context)
    response = render(request, 'df_goods/detail.html', context)

    #使用cookies记录最近浏览的商品id, 然后在用户中心调用显示最近浏览记录
    # 获取记录最近浏览商品id的cookies, 和最新一次浏览记录比较
    # 若最新浏览商品已存在,则删掉cookies中的,将其插入到cookies最前面
    goods_ids = request.COOKIES.get('goods_ids')
    if goods_ids:
        # 分割出每个商品id
        goods_id_list = goods_ids.split(',')
        if goods_id_list.count(str(goodsid)) >= 1:
            goods_id_list.remove(str(goodsid))
        goods_id_list.insert(0, str(goodsid))
        # print(goods_id_list)
        # 判断列表数是否超过5个
        if len(goods_id_list) >= 6:
            # goods_id_list=good_id_list[0,5]
            goods_id_list.pop()
        # 还原cookies:将id合并
        # join函数就是字符串的函数,参数和插入的都要是字符串
        # .jion(str), jion分割的必须是字符串!!,如果传入的列表内都是str则没问题,但我们传的列表内是含有int的!所以会报类型错误!
        goods_ids = ','.join(goods_id_list)
    else:
        # 第一次添加，直接追加
        goods_ids = str(goodsid)
    # print(goods_ids)

    response.set_cookie('goods_ids', goods_ids)
    return response


# 自定义search上下文
class MySearchView(SearchView):
    def extra_context(self):
        context = super(MySearchView, self).extra_context()
        context['guest_cart'] = True
        get_cartcount(self.request)
        return context
