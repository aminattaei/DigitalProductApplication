from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.apps import apps

class BaseMetaModel(models.base.ModelBase):
    def __new__(cls, name, bases, attrs, **kwargs):
        new_class = super().__new__(cls, name, bases, attrs, **kwargs)

        if not any(isinstance(base, BaseMetaModel) for base in bases):
            return new_class

        app_label = new_class._meta.app_label
        class Meta:
            abstract = False
            db_table = f"{app_label}_{name.lower()}"
            verbose_name = _(name)
            verbose_name_plural = _(name + "s")
        setattr(new_class, 'Meta', Meta)
        return new_class

class BaseDigitalModel(models.Model, metaclass=BaseMetaModel):
    title = models.CharField(_("title"), max_length=50)
    avatar = models.ImageField(_("avatar"), upload_to='%(class)s/avatar/', blank=True, null=True)
    is_enable = models.BooleanField(_("is enable"), default=True)
    created_at = models.DateTimeField(_("created time"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated time"), auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(f"{self.__class__.__name__}_detail", kwargs={"pk": self.pk})

class Category(BaseDigitalModel):
    parent = models.ForeignKey('self', verbose_name=_("parent"), blank=True, null=True, on_delete=models.CASCADE)
    description = models.TextField(_("description"), blank=True)

class Product(BaseDigitalModel):
    description = models.TextField(_("description"), blank=True)
    categories = models.ManyToManyField(Category, verbose_name=_("categories"), blank=True)
    stars = models.IntegerField(_("star count"),default=0,blank=True)
    price = models.IntegerField(_("price"))
    is_stock = models.BooleanField(_("in stock?"),default=True)
    is_new = models.BooleanField(_("is new product?"),default=False)
    is_off = models.BooleanField(_("product have off?"),default=False)
    off_price = models.CharField(_("off price"), max_length=50,blank=True,null=True)
    
    def stars_range(self):
        return range(self.stars)

class File(BaseDigitalModel):
    product = models.ForeignKey(Product, verbose_name=_("product"), on_delete=models.CASCADE)
    file = models.FileField(_("file"), upload_to='files/%Y/%m/%d/', max_length=100)
