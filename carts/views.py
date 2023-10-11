from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required 

from shop.models import Product, Variation
from carts.models import Cart, CartItem

def get_cart_id(request):
    cart_id = request.session.session_key
    if not cart_id:
        cart_id = request.session.create()
    return cart_id


def cart_page(request, quantity=0, total=0, cart_items=None):
    grand_total = tax = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (5 * total) / 100
        grand_total = total + tax 
    except ObjectDoesNotExist:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "grand_total": grand_total,
        "tax": tax
    }
    return render(request, "store/cart.html", context=context)

def add_cart(request, product_id):
    current_user = request.user
    product = Product.objects.get(id=product_id)
    if current_user.is_authenticated:
        product_variations = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except:
                    pass

        exist_cart_item = CartItem.objects.filter(product=product, user=current_user).exists()
        if exist_cart_item:
            cart_items = CartItem.objects.filter(product=product, user=current_user)
            exist_cart_variation = []
            product_id_list = []
            for item in cart_items:
                item_variations = item.variations.all()
                exist_cart_variation.append(list(item_variations))
                product_id_list.append(item.id)

            if product_variations in exist_cart_variation:
                item_index = exist_cart_variation.index(product_variations)
                item_id = product_id_list[item_index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(product=product, user=current_user, quantity=1)
                cart_item.variations.clear()
                cart_item.variations.add(*product_variations)
        else:
            cart_item = CartItem.objects.create(product=product, user=current_user, quantity=1)
            cart_item.variations.clear()
            cart_item.variations.add(*product_variations)
        cart_item.save()
        return redirect("cart")
    else:
        product_variations = []
        if request.method == "POST":
            for item in request.POST:
                key = item
                value = request.POST[key]
                try:
                    variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                    product_variations.append(variation)
                except:
                    pass

        try:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(
                cart_id = get_cart_id(request)
            )
        cart.save()

        exist_cart_item = CartItem.objects.filter(product=product, cart=cart).exists()
        if exist_cart_item:
            cart_items = CartItem.objects.filter(product=product, cart=cart)
            exist_cart_variation = []
            product_id_list = []
            for item in cart_items:
                item_variations = item.variations.all()
                exist_cart_variation.append(list(item_variations))
                product_id_list.append(item.id)

            if product_variations in exist_cart_variation:
                item_index = exist_cart_variation.index(product_variations)
                item_id = product_id_list[item_index]
                cart_item = CartItem.objects.get(product=product, id=item_id)
                cart_item.quantity += 1
            else:
                cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
                cart_item.variations.clear()
                cart_item.variations.add(*product_variations)
        else:
            cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
            cart_item.variations.clear()
            cart_item.variations.add(*product_variations)
        cart_item.save()
        return redirect("cart")

def remove_cart(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect("cart")

def remove_cart_item(request, product_id, cart_item_id):
    product = Product.objects.get(id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=get_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect("cart")

@login_required(login_url="login")
def checkout(request, quantity=0, total=0, cart_items=None):
    grand_total = tax = 0
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (5 * total) / 100
        grand_total = total + tax 
    except ObjectDoesNotExist:
        pass
    context = {
        "total": total,
        "quantity": quantity,
        "cart_items": cart_items,
        "grand_total": grand_total,
        "tax": tax
    }
    return render(request, "store/checkout.html", context=context)
