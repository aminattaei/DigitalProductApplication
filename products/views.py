from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib import messages
from django.contrib.auth import authenticate
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.db import transaction


from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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
from .forms import CheckoutForm, CommentForm, LoginForm
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


# -------------- Standard Views --------------


def home_page(request):
    """Render home page with all products and categories"""
    products = Product.objects.all()
    categories = Category.objects.all()
    return render(
        request, "index.html", {"products": products, "categories": categories}
    )


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


# -------------- Add To cart View -------------------


@login_required(login_url="/login/")
def add_multiple_to_cart(request):
    """
    Add multiple products to the user's shopping cart in a single transaction.
    Expects POST data in the format:
        product_ids: list of product IDs
        quantities: list of corresponding quantities
    All additions are atomic: either all succeed or none.
    """
    user = request.user

    # Ensure Customer object exists for the logged-in user
    customer, _ = Customer.objects.get_or_create(
        user=user,
        defaults={
            "first_name": getattr(user, "first_name", "FirstName"),
            "last_name": getattr(user, "last_name", "LastName"),
            "email": getattr(user, "email", "example@example.com"),
            "phone": "00000000000",
        },
    )

    product_ids = request.POST.getlist("product_ids")
    quantities = request.POST.getlist("quantities")

    if not product_ids or not quantities or len(product_ids) != len(quantities):
        messages.error(request, "Invalid product data submitted.")
        return redirect("cart_page")  # یا هر صفحه مناسب

    try:
        with transaction.atomic():
            # Get or create cart
            cart, _ = Cart.objects.get_or_create(customer=customer)

            for prod_id, qty in zip(product_ids, quantities):
                product = get_object_or_404(Product, pk=int(prod_id))
                quantity = max(int(qty), 1)  # Ensure at least 1

                # Get or create cart item
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if created:
                    cart_item.quantity = quantity
                else:
                    cart_item.quantity += quantity

                cart_item.save()

        messages.success(request, "All selected products have been added to your cart!")

    except Exception as e:
        messages.error(request, f"An error occurred while adding products: {str(e)}")

    return redirect("cart_page")


# -------------- Cart Summary View ------------------

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem, Customer, Product
from django.db import transaction

@login_required(login_url="/login/")
def cart_summary_view(request):
    """
    Display the user's shopping cart with all items, quantities, and total prices.
    Allows updating quantities or removing items via separate views.
    """
    user = request.user

    # Ensure a Customer exists for the user
    customer, _ = Customer.objects.get_or_create(
        user=user,
        defaults={
            "first_name": getattr(user, "first_name", "FirstName"),
            "last_name": getattr(user, "last_name", "LastName"),
            "email": getattr(user, "email", "example@example.com"),
            "phone": "00000000000",  # Default value if not set
        }
    )

    # Ensure the user's cart exists
    cart, _ = Cart.objects.get_or_create(customer=customer)

    # Calculate total price for the cart
    total_price = sum(item.get_total_price() for item in cart.items.all())

    context = {
        "cart": cart,
        "cart_items": cart.items.all(),  # Access CartItem objects in template
        "total_price": total_price,
    }

    return render(request, "cart_summary.html", context)



# -------------- Update Cart View --------------


from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CartItem, Cart, Customer

@login_required(login_url="/login/")
def update_cart_item(request, item_id):
    """
    Update quantity of a specific item in the user's cart.
    If quantity is set to 0, remove the item from the cart.
    """
    user = request.user

    # Ensure Customer exists
    customer, _ = Customer.objects.get_or_create(
        user=user,
        defaults={
            "first_name": getattr(user, "first_name", "FirstName"),
            "last_name": getattr(user, "last_name", "LastName"),
            "email": getattr(user, "email", "example@example.com"),
            "phone": "00000000000",
        },
    )

    # Ensure Cart exists
    cart, _ = Cart.objects.get_or_create(customer=customer)

    # Get the CartItem to update
    cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

    if request.method == "POST":
        try:
            quantity = int(request.POST.get("quantity", cart_item.quantity))
        except ValueError:
            messages.error(request, "Invalid quantity entered.")
            return redirect("cart_page")

        if quantity <= 0:
            cart_item.delete()
            messages.success(request, f"Removed {cart_item.product.title} from your cart.")
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f"Updated quantity for {cart_item.product.title}.")

    return redirect("cart_page")


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

    if request.method == "POST":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, "You must be logged in to submit a comment.")
            return redirect("login_page")

        # Ensure a Customer object exists for the logged-in user
        customer, created = Customer.objects.get_or_create(
            user=request.user,
            defaults={
                "first_name": getattr(request.user, "first_name", "FirstName"),
                "last_name": getattr(request.user, "last_name", "LastName"),
                "email": getattr(request.user, "email", "example@example.com"),
                "phone": "00000000000",  # Default value
            },
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
                text=form.cleaned_data["text"],
                stars=form.cleaned_data["stars"],
                is_approved=False,  # Set True if you want to auto-approve
            )
            messages.success(
                request,
                "Your comment has been registered and will be displayed after admin approval.",
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

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user:
            messages.success(request, f"Welcome back, {username}!")
            return redirect("home_page")
        else:
            messages.error(
                request,
                "The username or password is incorrect! Please try again or contact support.",
            )

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
