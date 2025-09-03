
from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('products',views.ProductViewSet,basename='product-viewset')

urlpatterns = [
    path('',views.HomeProductListView.as_view(),name='home_page'),
    path('checkout/',views.CheckoutFormView.as_view(),name='checkout_page'),
    path('product/',views.ProductListView.as_view(),name='shop_page'),
    path('api/',include(router.urls))
]


