from django.db import models
from user_app.models import User
from django.core.validators import MinValueValidator
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
from django.core.files.storage import FileSystemStorage


def image_default():
    fss = FileSystemStorage()
    folder_path = "product/defaults/"
    try:
        filename = fss.listdir(folder_path)[1][0]
        return folder_path + filename
    except Exception as e:
        print(e)


class Product(models.Model):
    created_by = models.ForeignKey(
        User,
        related_name="products",
        on_delete=models.CASCADE,
        verbose_name=("Created By"),
    )
    title = models.CharField(
        max_length=250,
        verbose_name=("Title"),
    )
    slug = models.SlugField(
        max_length=255,
        verbose_name=("Slug"),
        unique=True,
        blank=True,
        null=True,
    )
    description = models.CharField(
        max_length=255,
        verbose_name=("Description"),
    )
    image = models.ImageField(
        upload_to="product/%m/%d",
        verbose_name=("Image"),
        blank=True,
        null=True,
        default=image_default,
    )
    stock = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    unit = models.CharField(max_length=255, default="piece")
    price = MoneyField(
        max_digits=20,
        decimal_places=2,
        default_currency="USD",
        verbose_name=("Price"),
        validators=[MinMoneyValidator(1), MaxMoneyValidator(5000000)],
    )
    country = CountryField(
        blank_label="(select country)",
        null=True,
        blank=True,
        verbose_name=("Country Name"),
    )
