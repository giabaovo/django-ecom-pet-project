from django.urls import path

from carts import views

urlpatterns = [
    path('', views.cart_page, name="cart"),
    path('add_item/<int:product_id>', views.add_cart, name="add_cart"),
    path('remove_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name="remove_cart"),
    path('remove_cart_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name="remove_cart_item"),
    path('checkout/', views.checkout, name="checkout"),
]