from django.db import models

CATEGORY = {
    "mobile": "Mobile",
    "laptop": "Laptop",
    "top_wear": "Top Wear",
    "bottom_wear": "Bottom Wear",
}


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices=CATEGORY, max_length=100)
    product_image = models.ImageField(upload_to="product_images")

    def save(self, *args, **kwargs):
        self.brand = self.brand.lower()
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id}"
