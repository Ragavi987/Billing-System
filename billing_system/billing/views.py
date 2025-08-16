from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib import messages
from .models import Product, Customer, Purchase, PurchaseItem

DENOMINATIONS = [500, 50, 20, 10, 5, 2, 1]

def calculate_change(change_amount):
    result = {}
    for denom in DENOMINATIONS:
        count, change_amount = divmod(change_amount, denom)
        if count > 0:
            result[denom] = int(count)
    return result

@transaction.atomic
def billing_view(request):
    if request.method == "GET":
        product_qs = Product.objects.all()
        print("product_qs", product_qs)

        return render(request, "billing_form.html", {
            "product_qs": product_qs
        })

    if request.method == "POST":
        email = request.POST.get("customer_email")
        paid_amount = float(request.POST.get("paid_amount", 0))

        product_ids = request.POST.getlist("product_id")
        quantities = request.POST.getlist("quantity")

        if not email:
            messages.error(request, "Customer email is required.")
            return redirect("billing:billing")

        customer, _ = Customer.objects.get_or_create(email=email)
        purchase = Purchase.objects.create(customer=customer, paid_amount=paid_amount)

        total_without_tax = 0
        total_tax = 0

        for pid, qty in zip(product_ids, quantities):
            if not pid.strip():
                continue
            qty = int(qty)
            product = get_object_or_404(Product, product_id=pid)
            if product.available_stocks < qty:
                messages.error(request, f"Not enough stock for {product.name}")
                return redirect("billing:billing")

            product.available_stocks -= qty
            product.save()

            subtotal = product.price_per_unit * qty
            tax_amount = subtotal * (product.tax_percentage / 100)

            PurchaseItem.objects.create(
                purchase=purchase,
                product=product,
                quantity=qty,
                price_at_purchase=product.price_per_unit,
                tax_at_purchase=product.tax_percentage
            )

            total_without_tax += subtotal
            total_tax += tax_amount

        total_with_tax = total_without_tax + total_tax
        rounded_total = int(total_with_tax)
        balance = int(paid_amount - rounded_total)

        purchase.total_amount = total_with_tax
        purchase.save()

        change_distribution = calculate_change(balance)

        return render(request, "billing_result.html", {
            "purchase": purchase,
            "items": purchase.items.all(),
            "total_without_tax": total_without_tax,
            "total_tax": total_tax,
            "rounded_total": rounded_total,
            "balance": balance,
            "change_distribution": change_distribution

        })

    return render(request, "billing_form.html")

