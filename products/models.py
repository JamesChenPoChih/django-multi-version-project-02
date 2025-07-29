
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    image = models.CharField(max_length=255)  # 圖片路徑
    quantity = models.PositiveIntegerField(default=1000)  # 🆕 新增庫存數量

    def __str__(self):
        return self.name