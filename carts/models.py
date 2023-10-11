from django.db import models

from shop.models import Product, Variation

from accounts.models import Account

class Cart(models.Model):
    cart_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id
    

class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def get_sub_total(self):
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product
    
