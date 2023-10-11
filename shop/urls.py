from django.urls import path
from shop import views

urlpatterns = [
    path('', views.home, name="home"),
    path('store/', views.store, name="store"),
    path('store/category/<slug:category_slug>/', views.store, name="product_by_category"),
    path('store/category/<slug:category_slug>/product/<slug:product_slug>/', views.product_detail, name="product_detail"),
    path('store/search/', views.product_search, name="product_search"),
    path('store/submit_review/<product_id>', views.submit_review, name="submit_review"),
]