from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path("billing/", views.billing_view, name="billing"),
]
