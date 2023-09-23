from django.contrib import admin
from django.db import transaction

from courses.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "created", "updated")
    search_fields = ("name", "owner")


admin.site.register(Product, ProductAdmin)