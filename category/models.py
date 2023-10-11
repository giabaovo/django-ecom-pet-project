from django.db import models
from django.urls import reverse

class CategoryModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to="photos/categories", blank=True)

    def __str__(self):
        return self.name
    
    def get_url(self):
        return reverse("product_by_category", args=[self.slug])

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"