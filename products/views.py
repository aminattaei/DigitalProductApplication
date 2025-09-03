from django.shortcuts import render

from .models import Category,File,Product

def home_page(request):
    return render(request,'index.html',{})


def checkout_page(request):
    return render(request,'checkout.html',{})

def shop_page(request):
    products = Product.objects.all()
    return render(request,'store.html',{'products':products})

def product_page(request):
    return render(request,'product.html',{})

def blank_page(request):
    return render(request,'blank.html',{})