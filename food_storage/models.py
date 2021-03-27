from django.db import models


class FoodCategory(models.Model):
    name = models.CharField(max_length=20)

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
    name = models.CharField(max_length=30)
    category = models.ForeignKey(FoodCategory, on_delete=models.SET_NULL, null=True)
    food_group = models.CharField(max_length=2, choices=FOOD_GROUPS)
    carbohydrates = models.FloatField()
    fats = models.FloatField()
    protein = models.FloatField()
    quantity = models.IntegerField(default=1)
    standard_portion = models.IntegerField(null=True)

    def __str__(self):
        return self.name
