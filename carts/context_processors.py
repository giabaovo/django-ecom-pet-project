from carts.models import Cart, CartItem
from carts.views import get_cart_id

def cart_counter(request):
    if "admin" in request.path:
        return {}
    else:
        try:
            cart_count = 0
            if request.user.is_authenticated:
                cart_items = CartItem.objects.filter(user=request.user)
            else:
                cart = Cart.objects.filter(cart_id=get_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
        return {"cart_count": cart_count}
