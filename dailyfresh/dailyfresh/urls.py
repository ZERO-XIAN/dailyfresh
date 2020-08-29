"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('df_user.urls')),  # 用户
    path('tinymce', include('tinymce.urls')),  # 富文本编辑器-商品详情
    path('', include(('df_goods.urls', 'df_goods'), namespace='goods')),
    path('goods/', include('df_goods.urls')),
    path('cart/', include('df_cart.urls')),
    path('order/', include('df_order.urls')),
    # path('search/', include('haystack.urls')),
]
