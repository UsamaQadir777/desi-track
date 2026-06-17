from django.db import models
from django.utils.text import slugify


class FoodCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    icon = models.CharField(max_length=80, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "food categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    SERVING_GRAMS = "grams"
    SERVING_QUANTITY = "quantity"
    SERVING_CHOICES = [
        (SERVING_GRAMS, "Per 100g"),
        (SERVING_QUANTITY, "Per Quantity"),
    ]

    category = models.ForeignKey(FoodCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, blank=True)
    serving_type = models.CharField(max_length=20, choices=SERVING_CHOICES, default=SERVING_GRAMS)
    quantity_label = models.CharField(max_length=60, blank=True, default="")
    icon = models.CharField(max_length=80, blank=True, default="")
    serving_size_grams = models.DecimalField(max_digits=7, decimal_places=2, default=100)
    calories = models.DecimalField(max_digits=8, decimal_places=2, help_text="Calories per 100g or per quantity")
    protein = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Protein grams per 100g or per quantity")
    carbs = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Carbs grams per 100g or per quantity")
    fat = models.DecimalField(max_digits=8, decimal_places=2, default=0, help_text="Fat grams per 100g or per quantity")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category__name", "name"]
        unique_together = ("category", "name")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
