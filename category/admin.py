from django.contrib import admin

from category.models import CategoryModel

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "image"]
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(CategoryModel, CategoryAdmin)