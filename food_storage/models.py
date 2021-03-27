from django.db import models

class FoodCategory(models.Model):
    name = models.Charfield(max_length=20)

    def __str__(self):
        return self.name