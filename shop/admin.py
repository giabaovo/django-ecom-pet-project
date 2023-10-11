import admin_thumbnails

from django.contrib import admin

from shop.models import Product, Variation, ReviewRating, ProductGallery

@admin_thumbnails.thumbnail("image")
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "slug", "stock", "category", "is_available"]
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ["product", "variation_category", "variation_value", "is_active"]

class ReviewRatingAdmin(admin.ModelAdmin):
    list_display = ("title", "content", "rating")

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)
admin.site.register(ReviewRating, ReviewRatingAdmin)
admin.site.register(ProductGallery)

