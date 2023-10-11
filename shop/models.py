from django.db import models
from django.db.models import Avg, Count

from category.models import CategoryModel

from accounts.models import Account

class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.PositiveIntegerField()
    stock = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to="photos/products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)

    def product_average_review(self):
        review = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg("rating"))
        average_point = float(review["average"]) if review["average"] is not None else 0
        return average_point
    
    def product_review_count(self):
        review = ReviewRating.objects.filter(product=self, status=True).aggregate(review_total=Count("id"))
        review_total = int(review["review_total"])
        return review_total


    def __str__(self):
        return self.name

class VariationManage(models.Manager):
    def get_color(self):
        return super(VariationManage, self).filter(variation_category="color", is_active=True)
    
    def get_size(self):
        return super(VariationManage, self).filter(variation_category="size", is_active=True)

class Variation(models.Model):

    variation_category_choices = (
        ("size", "size"),
        ("color", "color"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation_category = models.CharField(max_length=255, choices=variation_category_choices)
    variation_value = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = VariationManage()

    def __str__(self):
        return self.variation_value
    
class ReviewRating(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True)
    content = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="photos/products")

    def __str__(self):
        return self.product.name