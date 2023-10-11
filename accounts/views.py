from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator 
from django.core.mail import EmailMessage 

from accounts.forms import RegisterForm, UserProfileForm, AccountForm
from accounts.models import Account, UserProfile

from carts.models import Cart, CartItem
from carts.views import get_cart_id

from orders.models import Order, OrderItem

import requests

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            email = form.cleaned_data["email"]
            phone_number = form.cleaned_data["phone_number"]
            password = form.cleaned_data["password"]
            username = email.split("@")[0]
            user = Account.objects.create_user(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
            user.phone_number = phone_number
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Please active your account"
            mail_content = render_to_string("accounts/account_verification_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject, mail_content, to=[to_email])
            send_email.send()
            return redirect("/accounts/register/?verify=true&email="+email)
    else:
        form = RegisterForm()
    return render(request, "accounts/register.html", context={"form": form})

def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        user = authenticate(email=email, password=password)
        if user:
            try:
                cart = Cart.objects.get(cart_id=get_cart_id(request))
                is_cart_item_exist = CartItem.objects.filter(cart=cart).exists()
                if is_cart_item_exist:
                    cart_items = CartItem.objects.filter(cart=cart)

                    product_variation = []
                    for item in cart_items:
                        item_variation = item.variations.all()
                        product_variation.append(list(item_variation))

                    cart_items_by_user = CartItem.objects.filter(user=user)
                    product_ex_variation = []
                    item_id = []
                    for item in cart_items_by_user:
                        exist_item_variation = item.variations.all()
                        product_ex_variation.append(list(exist_item_variation))
                        item_id.append(item.id)

                    for pr in product_variation:
                        if pr in product_ex_variation:
                            index = product_ex_variation.index(pr)
                            item_id = item_id[index]
                            cart_item = CartItem.objects.get(id=item_id)
                            cart_item.user = user
                            cart_item.quantity += 1
                            cart_item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass
            auth.login(request, user)
            url = request.META.get("HTTP_REFERER")
            try:
                query = requests.utils.urlparse(url).query
                params = dict(x.split("=") for x in query.split("&"))
                if "next" in params:
                    return redirect(params["next"])
            except:
                return redirect("home")
        else:
            messages.error(request, "Invalid Login Credential")
            return redirect("login")
    return render(request, "accounts/login.html")

@login_required(login_url="login")
def logout(request):
    auth.logout(request)
    return redirect("home")

def active(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(id=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulations! Your account is activated")
        return redirect("login")
    messages.error(request, "Activate your account fail")
    return redirect("register")

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        user_email_exist = Account.objects.filter(email=email).exists()
        if user_email_exist:
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset password"
            mail_content = render_to_string("accounts/reset_password_email.html", {
                "user": user,
                "domain": current_site,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user)
            })
            email_to = email
            sent_email = EmailMessage(mail_subject, mail_content, to=[email_to])
            sent_email.send()
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, "Account with this email does not exist")
            return redirect("forgot_password")
    return render(request, "accounts/forgot_password.html")

def reset_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(id=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session["uid"] = uid
        messages.success(request, "Please reset your password")
        return redirect("reset_password")
    else:
        messages.error(request, "This link has been expired")
        return redirect("forgot_password")

def reset_password(request):
    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password == confirm_password:
            uid = request.session["uid"]
            user = Account._default_manager.get(id=uid)
            user.set_password(password)
            user.save()
            messages.success(request, "Reset password successfully")
            return redirect("login")
        else:
            messages.error(request, "Password does not match")
            return redirect("reset_password")
    return render(request, "accounts/reset_password.html")

@login_required(login_url="login")
def dashboard(request):
    order = Order.objects.filter(user__id=request.user.id, is_orderd=True).order_by("-created_at")
    order_total = order.count()
    user_profile = UserProfile.objects.get(user=request.user)
    context = {
        "order_total": order_total,
        "user_profile": user_profile
    }
    return render(request, "accounts/dashboard.html", context=context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user, is_orderd=True).order_by("-created_at")
    context = {
        "orders": orders
    }
    return render(request, "accounts/my_orders.html", context=context)

def edit_profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == "POST":
        account_form = AccountForm(request.POST, instance=request.user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if account_form.is_valid() and user_profile_form.is_valid():
            account_form.save()
            user_profile_form.save()
            messages.success(request, "Your Profile Has Been Updated")
            return redirect("edit_profile")
    else:
        account_form = AccountForm(instance=request.user)
        user_profile_form = UserProfileForm(instance=user_profile)
    context = {
        "account_form": account_form,
        "user_profile_form": user_profile_form,
        "user_profile": user_profile
    }
    return render(request, "accounts/edit_profile.html", context=context)

def change_password(request):
    if request.method == "POST":
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = Account.objects.get(username__exact=request.user.username)
        if new_password == confirm_password:
            if user.check_password(current_password):
                user.set_password(new_password)
                user.save()
                messages.success(request, "Your password has been updated")
                return redirect("login")
            else:
                messages.error(request, "Invalid current password")
        else:
            messages.error(request, "Password didn't match")
            return redirect("change_password")
    return render(request, "accounts/change_password.html")

def order_detail(request, order_id):
    order_product = OrderItem.objects.filter(order__order_number=order_id)
    order = Order.objects.get(order_number=order_id)
    total = 0
    for item in order_product:
        total += item.quantity * item.product_price
    context = {
        "order_product": order_product,
        "order": order,
        "total": total
    }
    return render(request, "accounts/order_detail.html", context=context)