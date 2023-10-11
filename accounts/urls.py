from django.urls import path
from accounts import views

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('active/<uidb64>/<token>/', views.active, name="active"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('my_orders/', views.my_orders, name="my_orders"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),

    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name="reset_password_validate"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path('change_password/', views.change_password, name="change_password"),
    path('order_detail/<int:order_id>', views.order_detail, name="order_detail"),
]