from django.urls import path
from . import views

urlpatterns = [
    path('',views.order),
    path('order_handle/', views.order_handle),
    path('pay&<int:orderid>/', views.pay),
    path('viewlog&<int:orderid>/', views.viewlog),
]