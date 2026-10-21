from django.contrib import admin
from .models import Order, InvoiceItem, TopPurchaser, MostMoviesPurchased
from django.contrib.auth.models import User
from django.db.models import Sum
from django.template.response import TemplateResponse

class TopPurchaserAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
            return False

    def has_delete_permission(self, request, obj=None):
            return False

    def changelist_view(self, request, extra_context = None):
          purchasers = (
                User.objects.annotate(purchase_count=Sum("order__invoiceitem__quantity"))
                .order_by("-purchase_count", "username")
          )
          size = request.GET.get("size")
          if size and size.isdigit():
                purchasers = purchasers[:int(size)]

          context = {
                **self.admin_site.each_context(request),
                "title": "Top Purchasers",
                "purchasers": purchasers
          }
          return TemplateResponse(request, "admin/cart/top_purchasers.html", context)

class MostMoviesPurchasedAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
            return False

    def has_delete_permission(self, request, obj=None):
            return False

    def changelist_view(self, request, extra_context = None):
          qty = Sum("order__invoiceitem__quantity")
          buyers = (
                User.objects.annotate(movies_purchased=qty)
                .filter(movies_purchased__gt = 0)
                .order_by("-movies_purchased", "username")
          )
          top_count = buyers[0].movies_purchased if buyers else 0
          top_users = [
                u for u in buyers if u.movies_purchased == top_count
          ]
          context = {
                **self.admin_site.each_context(request),
                "title": "Most Movies Purchased",
                "top_users": top_users,
                "top_count": top_count,
          }
          return TemplateResponse(request, "admin/cart/most_movies_purchased.html", context)


# Register your models here.
admin.site.register(TopPurchaser, TopPurchaserAdmin)
admin.site.register(Order)
admin.site.register(InvoiceItem)
admin.site.register(MostMoviesPurchased, MostMoviesPurchasedAdmin)