from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.conf.urls.static import static
from django.utils import timezone


class BaseDigitalModel(models.Model):
    title = models.CharField(_("title"), max_length=50)
    description = models.TextField(_("description"), blank=True)
    avatar = models.ImageField(
        _("avatar"), upload_to="%(class)s/avatar/", blank=True, null=True
    )
    is_enable = models.BooleanField(_("is enable"), default=True)
    created_at = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated time"), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self.__class__.__name__}_detail", kwargs={"pk": self.pk})

    def get_avatar_url(self):
        if self.avatar:
            return self.avatar
        else:
            return static("static/img/default_product.png")


class Category(BaseDigitalModel):
    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent"),
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")


class Product(BaseDigitalModel):
    categories = models.ManyToManyField(
        Category, verbose_name=_("categories"), blank=True
    )
    stars = models.IntegerField(_("star count"), default=0, blank=True)
    price = models.IntegerField(_("price"))
    is_stock = models.BooleanField(_("in stock?"), default=True)
    is_new = models.BooleanField(_("is new product?"), default=False)
    is_off = models.BooleanField(_("product have off?"), default=False)
    off_price = models.CharField(_("off price"), max_length=50, blank=True, null=True)

    def stars_range(self):
        return range(self.stars)

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")


class File(BaseDigitalModel):
    product = models.ForeignKey(
        Product, verbose_name=_("product"),related_name='images', on_delete=models.CASCADE
    )
    file = models.FileField(_("file"), upload_to="files/%Y/%m/%d/", max_length=100)

    class Meta:
        verbose_name = _("File")
        verbose_name_plural = _("Files")


class Customer(models.Model):
    first_name = models.CharField(_("first_name"), max_length=50)

    last_name = models.CharField(_("last_name"), max_length=50)

    phone = models.CharField(_("phone number"), max_length=11)

    email = models.EmailField(_("email"), max_length=254)

    class Meta:
        verbose_name = _("customer")
        verbose_name_plural = _("customers")

    def __str__(self):
        return self.first_name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.TextField()
    phone = models.CharField(max_length=11, blank=True)
    date = models.DateField(default=timezone.now())

    status = models.BooleanField(default=False)
    shipped_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _("order")
        verbose_name_plural = _("orders")

    def __str__(self):
        return f"Order #{self.id} by {self.customer.first_name}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.title}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Contact(models.Model):
    fullname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    message = models.TextField()

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    def __str__(self):
        return self.fullname

    def get_absolute_url(self):
        return reverse("Contact_detail", kwargs={"pk": self.pk})


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart #{self.id} - Customer: {self.customer.first_name}"

    def get_total_price(self):
        return sum(item.get_total_price() for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.product.price * self.quantity


class Comment(models.Model):
    product = models.ForeignKey(
        Product, verbose_name=_("product"), on_delete=models.CASCADE
    )
    customer = models.ForeignKey(
        Customer, verbose_name=_("customer"), on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        return f"Comment by {self.customer} on {self.product}"
