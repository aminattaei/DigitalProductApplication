from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", views.ProductViewSet, basename="product-viewset")
router.register("files", views.FileViewSet, basename="files-viewset")
router.register("categories", views.CategoryViewSet, basename="category-viewset")

router.register("carts", views.CartViewSet, basename="cart-viewset")
router.register("customers", views.CustomerViewSet, basename="customer-viewset")
router.register("orders", views.OrderViewSet, basename="order-viewset")
router.register("comments", views.CommentViewSet, basename="comment-viewset")
router.register("contacts", views.ContactViewSet, basename="contact-viewset")


urlpatterns = [
    path("", views.home_page, name="home_page"),
    path("checkout/", views.CheckoutFormView.as_view(), name="checkout_page"),
    path("products/", views.ProductListView.as_view(), name="shop_page"),
    path("product/<int:pk>/review/", views.review_model_view, name="product_review"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="Product_detail"),
    path("api/", include(router.urls)),
    path('register/',views.signUp_page,name="signup-page"),
    path('login/',views.login_page,name="login_page"),
]
