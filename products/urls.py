
from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.home_page,name='home_page'),
    path('checkout/',views.checkout_page,name='home_page'),
    path('product/',views.product_page,name='home_page'),
    path('shop/',views.shop_page,name='home_page'),
]


