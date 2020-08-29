from django.db import models
from tinymce.models import HTMLField

# 商品分类


class TypeInfo(models.Model):
    ttitle = models.CharField(max_length=20)
    isDelete = models.BooleanField(default=False)

    def __str__(self):
        return self.ttitle

# 商品


class GoodsInfo(models.Model):
    # 名称
    gtitle = models.CharField(max_length=20)

    # 图片位置    服务器部署记得看看
    gpic = models.ImageField(upload_to='df_goods')

    # 价格
    gprice = models.DecimalField(max_digits=5, decimal_places=2)

    # 是否下架
    isDelete = models.BooleanField(default=False)

    # 价格单位b
    gunit = models.CharField(max_length=20, default='500g')

    # 点击量  用于排序
    gclick = models.IntegerField()

    # 简介
    gjianjie = models.CharField(max_length=200)

    # 库存
    gstock = models.IntegerField()

    # 详细介绍(富文本编辑器)
    gcontent = HTMLField()

    # 广告
    # gadv = models.IntegerField()

    # 外键
    gtype = models.ForeignKey(TypeInfo, on_delete=models.CASCADE)

    def __str__(self):
        return self.gtitle
