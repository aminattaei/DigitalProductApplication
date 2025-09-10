from django.shortcuts import render,get_object_or_404
from django.urls import reverse_lazy
from django.views import generic

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .serializers import (
    CartSerializer,
    CategorySerializer,
    FileSerializer,
    OrderSerializer,
    ProductSerializer,
    CustomerSerializer,
    CommentSerializer,
    ContactSerializer,
)
from .models import (
    Category,
    Product,
    File,
    Cart,
    CartItem,
    Comment,
    Contact,
    Customer,
    Order,
    OrderItem,
)
from .forms import CheckoutForm


#  Views -->


def home_page(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "index.html", {"products": products,'categories':categories})


class HomeProductListView(generic.ListView):
    model = Product
    context_object_name = "product"
    template_name = "index.html"


class CheckoutFormView(generic.FormView):
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("home_page")


class ProductListView(generic.ListView):
    model = Product
    context_object_name = "products"
    template_name = "store.html"


class ProductDetailView(generic.DetailView):
    model = Product
    context_object_name = "product"
    template_name = "product.html"


# Api Viewsets -->


class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
