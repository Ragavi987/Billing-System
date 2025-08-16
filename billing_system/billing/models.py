from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    product_id = models.CharField(max_length=50, unique=True)
    available_stocks = models.PositiveIntegerField()
    price_per_unit = models.FloatField()
    tax_percentage = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.product_id})"

class Customer(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email

class Purchase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.FloatField(default=0)
    paid_amount = models.FloatField(default=0)

    def __str__(self):
        return f"Purchase #{self.id} - {self.customer.email}"


class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.FloatField()
    tax_at_purchase = models.FloatField()

    def subtotal_without_tax(self):
        return self.price_at_purchase * self.quantity

    def tax_amount(self):
        return self.subtotal_without_tax() * (self.tax_at_purchase / 100)

    def subtotal_with_tax(self):
        return self.subtotal_without_tax() + self.tax_amount()

