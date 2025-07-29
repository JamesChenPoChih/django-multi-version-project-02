from django.contrib import admin
# products/management/commands/seed_products.py
from django.core.management.base import BaseCommand
from products.models import Product
# products/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')  # ✅ 顯示 quantity


class Command(BaseCommand):
    help = 'Seed 6 demo products'

    def handle(self, *args, **kwargs):
        Product.objects.all().delete()  # 清空原本資料

        items = [
            ("Calendar", 200, "images/calendar.jpg"),
            ("Mug", 150, "images/mug.jpg"),
            ("T-shirt", 300, "images/tshirt.jpg"),
            ("Jacket", 800, "images/jacket.jpg"),
            ("Hat", 100, "images/hat.jpg"),
            ("Backpack", 500, "images/backpack.jpg"),
        ]

        for name, price, image in items:
            Product.objects.create(name=name, price=price, image=image)

        self.stdout.write(self.style.SUCCESS('Successfully seeded 6 products!'))

from django.contrib import admin
from .models import Product

