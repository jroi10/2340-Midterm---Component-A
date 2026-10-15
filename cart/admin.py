from django.contrib import admin
from .models import Order, InvoiceItem

# Register your models here.
admin.site.register(Order)
admin.site.register(InvoiceItem)