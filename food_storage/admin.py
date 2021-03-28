from django.contrib import admin

from food_storage.models import FoodCategory, FoodIngredient

admin.site.register(FoodCategory)
admin.site.register(FoodIngredient)
