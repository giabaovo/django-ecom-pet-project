from django.shortcuts import render, get_object_or_404, redirect
from django.core.exceptions import ObjectDoesNotExist 
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages 

from shop.models import Product, ReviewRating, ProductGallery
from shop.forms import ReviewRatingForm

from category.models import CategoryModel

from carts.models import Cart, CartItem
from carts.views import get_cart_id

from orders.models import OrderItem

def home(request):
    products = Product.objects.filter(is_available=True)
    return render(request, "home.html", context={"products": products})

def store(request, category_slug=None):
    products = Product.objects.filter(is_available=True).order_by("id")
    if category_slug:
        category = get_object_or_404(CategoryModel, slug=category_slug)
        products = products.filter(category=category).order_by("id")
    products_count = products.count()
    paginator = Paginator(products, 6)
    page = request.GET.get("page")
    products_page = paginator.get_page(page)
    context = {
        "products": products_page,
        "products_count": products_count
    }
    return render(request, "store/store.html", context=context)

def product_detail(request, category_slug, product_slug):
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=get_cart_id(request), product=product).exists()
    except Product.ObjectDoesNotExist as e:
        raise e
    
    if request.user.is_authenticated:
        try:
            order_item = OrderItem.objects.filter(user=request.user, product__id=product.id, is_orderd=True).exists()
        except OrderItem.DoesNotExist:
            order_item = None
    else:
        order_item = None

    reviews = ReviewRating.objects.filter(product__id=product.id, status=True)

    product_gallery = ProductGallery.objects.filter(product_id=product.id)

    return render(request, "store/product-detail.html", context={"product": product, "in_cart": in_cart, "order_item": order_item, "reviews": reviews, "product_gallery": product_gallery})


def product_search(request):
    if "keyword" in request.GET:
        search_keyword = request.GET.get("keyword", "")
        if search_keyword:
            products = Product.objects.filter(Q(description__icontains=search_keyword) | Q(name__icontains=search_keyword))
            products_count = products.count()
            paginator = Paginator(products, 6)
            page = request.GET.get("page")
            products_page = paginator.get_page(page)
            context = {
                "products": products_page,
                "products_count": products_count,
                "search": True,
                "search_keyword": search_keyword
            }
    return render(request, "store/store.html", context=context)

def submit_review(request, product_id):
    url = request.META.get("HTTP_REFERER")
    try:
        review = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
        form = ReviewRatingForm(request.POST, instance=review)
        form.save()
        messages.success(request, "Your Review Has Been Updated")
        return redirect(url)
    except ReviewRating.DoesNotExist:
        form = ReviewRatingForm(request.POST)
        if form.is_valid():
            data = ReviewRating()
            data.title = form.cleaned_data.get("title")
            data.content = form.cleaned_data.get("content")
            data.rating = form.cleaned_data.get("rating")
            data.user_id = request.user.id
            data.product_id = product_id
            data.save()
            messages.success(request, "Your Review Has Been Posted")
            return redirect(url)
