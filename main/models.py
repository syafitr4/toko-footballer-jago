import uuid
from django.db import models

class Product(models.Model):
    class Category(models.TextChoices):
        JERSEY    = "JERSEY", "Jersey"
        BOOTS     = "BOOTS", "Boots"
        BALL      = "BALL", "Ball"
        ACCESSORY = "ACCESSORY", "Accessory"
        TICKET    = "TICKET", "Match Ticket"

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.JERSEY,
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 6 field wajib (nama tepat sama)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    thumbnail = models.URLField()  # jangan blank/null agar sesuai tugas
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name
