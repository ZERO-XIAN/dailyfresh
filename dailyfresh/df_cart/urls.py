from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart),
    path('add<int:goodsid>_<int:count>/', views.add),
    path('edit<int:cartid>_<int:count>/', views.edit),
    path('delete<int:cartid>/', views.delete),

]
