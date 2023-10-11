from django.contrib import admin

from orders.models import Payment, Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("payment", "user", "product", "quantity", "product_price", "is_orderd",)

class OrderAdmin(admin.ModelAdmin):
    list_display = ["order_number", "full_name", "phone", "email", "city", "order_total", "tax", "status", "is_orderd", "created_at"]
    list_filter = ["status", "is_orderd"]
    search_fields = ["order_number", "first_name", "last_name", "phone", "email"]
    list_per_page = 20
    inlines = [OrderItemInline]

admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)

