from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic


from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAuthenticated

from .serializers import ProductSerializer
from .models import Category,File,Product
from .forms import CheckoutForm
#  Views -->

class HomeProductListView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = "index.html"

class CheckoutFormView(generic.FormView):
    template_name = 'checkout.html'
    form_class = CheckoutForm
    success_url = reverse_lazy('home_page')

class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'products'
    template_name = "store.html"


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "product.html"


# Api Views -->

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]