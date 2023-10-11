from django.contrib import admin

from carts.models import Cart, CartItem

class CartAdmin(admin.ModelAdmin):
    list_display = ["cart_id", "created_at"]

class CartItemAdmin(admin.ModelAdmin):
    list_display = ["product", "cart", "quantity", "is_active"]

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)

