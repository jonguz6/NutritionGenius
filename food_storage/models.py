from django.db import models


class FoodCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    class Meta:
        verbose_name = "Food Category"
        verbose_name_plural = "Food Categories"

    def __str__(self):
        return self.name


class FoodIngredient(models.Model):
    FOOD_GROUPS = [
        ("f", "Fruits"),
        ("v", "Vegetables"),
        ("g", "Grains"),
        ("p", "Protein Foods"),
        ("d", "Dairy"),
    ]
    name = models.CharField(max_length=30, unique=True)
    category = models.ForeignKey(FoodCategory,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True,
                                 related_name="Ingredients")
    food_group = models.CharField(max_length=2, choices=FOOD_GROUPS)
    carbohydrates = models.FloatField()
    fats = models.FloatField()
    protein = models.FloatField()
    calories = models.IntegerField()
    quantity = models.IntegerField(default=1)
    standard_portion = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Ingredient"

    def __str__(self):
        return self.name
