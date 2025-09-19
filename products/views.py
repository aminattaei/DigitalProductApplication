from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import (
    Category, Product, File, Cart, CartItem,
    Comment, Contact, Customer, Order, OrderItem
)
from .forms import CheckoutForm, CommentForm, LoginForm
from .serializers import (
    CartSerializer, CategorySerializer, FileSerializer,
    OrderSerializer, ProductSerializer, CustomerSerializer,
    CommentSerializer, ContactSerializer
)


# -------------- Standard Views --------------

def home_page(request):
    """Render home page with all products and categories"""
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(request, "index.html", {"products": products, "categories": categories})


class HomeProductListView(generic.ListView):
    """ListView for displaying products on home page"""
    model = Product
    context_object_name = "product"
    template_name = "index.html"

class ProductListView(generic.ListView):
    """ListView for displaying all products in store page"""
    model = Product
    context_object_name = "products"
    template_name = "store.html"


class ProductDetailView(generic.DetailView):
    """DetailView for a single product"""
    model = Product
    context_object_name = "product"
    template_name = "product.html"


class CheckoutFormView(generic.FormView):
    """FormView for checkout page"""
    template_name = "checkout.html"
    form_class = CheckoutForm
    success_url = reverse_lazy("home_page")


# -------------- Review / Comment View --------------

def review_model_view(request, pk):
    """
    Handle product reviews/comments:
    - Only authenticated users can comment
    - One comment per user per product
    - Comments require admin approval
    - Supports rating (stars)
    """
    
    # Get the product or return 404
    product = get_object_or_404(Product, pk=pk)

    # Bind POST data to CommentForm or create empty form for GET request
    form = CommentForm(request.POST or None)

    if request.method == 'POST':
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to submit a comment.")
            return redirect('login_page')

        # Ensure a Customer object exists for the logged-in user
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                "first_name": getattr(request.user, 'first_name', 'FirstName'),
                "last_name": getattr(request.user, 'last_name', 'LastName'),
                "email": getattr(request.user, 'email', 'example@example.com'),
                "phone": "00000000000",  # Default value
            }
        )

        # Check if the user already commented on this product
        if Comment.objects.filter(customer=customer, product=product).exists():
            messages.error(request, f"You have already commented on {product.title}.")
            return redirect(product.get_absolute_url())

        # Save new comment if form is valid
        if form.is_valid():
            Comment.objects.create(
                product=product,
                customer=customer,
                text=form.cleaned_data['text'],
                stars=form.cleaned_data['stars'],
                is_approved=False  # Set True if you want to auto-approve
            )
            messages.success(
                request,
                "Your comment has been registered and will be displayed after admin approval."
            )
            return redirect(product.get_absolute_url())
        else:
            # Form is invalid
            messages.error(request, "There was a problem with your form submission.")

    # For GET request or invalid POST: display the form and approved comments
    approved_comments = Comment.objects.filter(product=product, is_approved=True)
    avg_stars = approved_comments.aggregate(Avg("stars"))["stars__avg"] or 0

    context = {
        "product": product,
        "form": form,
        "comments": approved_comments,
        "avg_stars": avg_stars,
    }
    return render(request, "product.html", context)


# -------------- Authentication Views --------------

def login_page(request):
    """
    Handle user login:
    - Authenticates with username/email and password
    - Shows success or error messages
    """
    form = LoginForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            messages.success(request, f"Welcome back, {username}!")
            return redirect('home_page')
        else:
            messages.error(request, "The username or password is incorrect! Please try again or contact support.")

    return render(request, "registration/login.html", {"form": form})


def signUp_page(request):
    """Signup page placeholder"""
    pass


# -------------- API Viewsets --------------

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
