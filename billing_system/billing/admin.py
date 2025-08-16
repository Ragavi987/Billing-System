from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "product_id", "available_stocks")


admin.site.register(Product, ProductAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ("email",)


admin.site.register(Customer, CustomerAdmin)


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("customer", "total_amount", "paid_amount")


admin.site.register(Purchase, PurchaseAdmin)


class PurchaseItemAdmin(admin.ModelAdmin):
    list_display = ("purchase", "product", "quantity", "price_at_purchase", "tax_at_purchase")


admin.site.register(PurchaseItem, PurchaseItemAdmin)