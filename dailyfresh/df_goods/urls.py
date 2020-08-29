from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('list<int:typeid>_<int:pageindex>_<int:sort>/',views.goodlist),
    path('<int:goodsid>/', views.detail),
    path('search/' ,views.MySearchView()),
]