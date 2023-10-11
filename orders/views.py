import datetime, json

from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.http import JsonResponse

from carts.models import CartItem

from shop.models import Product

from orders.forms import OrderForm
from orders.models import Order, Payment, OrderItem


def payment(request):
    body = json.loads(request.body)
    order = Order.objects.get(user=request.user, is_orderd=False, order_number=body.get("orderId"))
    payment = Payment(
        user = request.user,
        payment_id = body.get("transId"),
        payment_method = body.get("paymentMethod"),
        status = body.get("status"),
        amount_paid = order.order_total
    )
    payment.save()
    order.payment = payment
    order.is_orderd = True
    order.save()

    cart_items = CartItem.objects.filter(user=request.user)
    for item in cart_items:
        order_item = OrderItem()
        order_item.order_id = order.id
        order_item.user_id = request.user.id
        order_item.payment = payment
        order_item.product_id = item.product.id
        order_item.quantity = item.quantity
        order_item.product_price = item.product.price
        order_item.is_orderd = True
        order_item.save()

        cart_item = CartItem.objects.get(id=item.id)
        cart_item_variation = cart_item.variations.all()
        order_item = OrderItem.objects.get(id=order_item.id)
        order_item.variation.set(cart_item_variation)
        order_item.save()

        product = Product.objects.get(id=item.product.id)
        product.stock -= item.quantity
        product.save()

    CartItem.objects.filter(user=request.user).delete()

    mail_subject = "Thank you for your order"
    mail_content = render_to_string("orders/order_recieved_email.html", {
        "user": request.user,
        "order": order
    })
    to_email = request.user.email
    mail = EmailMessage(mail_subject, mail_content, to=[to_email])
    mail.send()

    data = {
        "order_number": order.order_number,
        "transId": payment.payment_id
    }

    return JsonResponse(data)

def place_order(request, total=0, quantity=0):
    current_user = request.user

    cart_items = CartItem.objects.filter(user=current_user)
    cart_item_amount = cart_items.count()
    if cart_item_amount < 0:
        return redirect("store")
    grand_total = tax = 0
    for item in cart_items:
        total += (item.product.price * item.quantity)
        quantity += item.quantity
    tax = (5 * total) / 100
    grand_total = total + tax 
    
    if request.method == "POST":
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            data = Order()
            data.user = current_user
            data.first_name = order_form.cleaned_data.get("first_name")
            data.last_name = order_form.cleaned_data.get("last_name")
            data.email = order_form.cleaned_data.get("email")
            data.phone = order_form.cleaned_data.get("phone")
            data.address_line_1 = order_form.cleaned_data.get("address_line_1")
            data.address_line_2 = order_form.cleaned_data.get("address_line_2")
            data.country = order_form.cleaned_data.get("country")
            data.state = order_form.cleaned_data.get("state")
            data.city = order_form.cleaned_data.get("city")
            data.order_note = order_form.cleaned_data.get("order_note")
            data.ip = request.META.get("REMOTE_ADDR")
            data.order_total = grand_total
            data.tax = tax
            data.save()
            current_year = int(datetime.date.today().strftime("%Y"))
            current_month = int(datetime.date.today().strftime("%m")) 
            current_date = int(datetime.date.today().strftime("%d"))
            d = datetime.date(current_year, current_month, current_date)
            current_time = d.strftime("%Y%m%d")
            order_number = current_time + str(data.id)
            data.order_number = order_number
            data.save()
            order = Order.objects.get(user=current_user, is_orderd=False, order_number=order_number)
            context = {
                "order": order,
                "cart_items": cart_items,
                "total": total,
                "grand_total": grand_total,
                "tax": tax
            }
            return render(request, "orders/payment.html", context=context)
    else:
        return redirect("checkout")

def order_complete(request):
    order_number = request.GET.get("order_number")
    transId = request.GET.get("payment_id")

    try:
        order = Order.objects.get(order_number=order_number, is_orderd=True)
        order_product = OrderItem.objects.filter(order_id=order.id)

        sub_total = 0
        for item in order_product:
            sub_total += item.product_price * item.quantity

        payment = Payment.objects.get(payment_id=transId)
        context = {
            "order_number": order_number,
            "sub_total": sub_total,
            "order": order,
            "transID": payment.payment_id,
            "payment": payment,
            "ordered_products": order_product
        }
    except(Payment.DoesNotExist, Order.DoesNotExist):
        return redirect("home")

    return render(request, "orders/order_complete.html", context=context)

