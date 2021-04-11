from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from food_storage.models import FoodIngredient


class FoodItem(models.Model):
    ingredient = models.ForeignKey(FoodIngredient,
                                   related_name="food_items",
                                   on_delete=models.PROTECT)
    quantity = models.FloatField(default=1)
    
    @property
    def calories(self):
        return self.ingredient.calories * self.quantity

    @property
    def carbs(self):
        return self.ingredient.carbohydrates * self.quantity

    @property
    def fats(self):
        return self.ingredient.fats * self.quantity

    @property
    def protein(self):
        return self.ingredient.protein * self.quantity

    def __str__(self):
        return f"{self.ingredient.__str__()} q:{self.quantity}"


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile",
                                primary_key=True)
    weight = models.FloatField()
    height = models.IntegerField()
    daily_food = models.ManyToManyField(FoodItem,
                                        through="UserFoodStorage",
                                        related_name="daily_food")
    calorie_goal = models.IntegerField(null=True)

    @property
    def daily_food_items(self):
        for item in self.food_storage.filter(date=date.today()):
            yield item

    @property
    def calories_today(self):
        calories = 0
        for item in self.daily_food_items:
            calories += item.food.calories
        return calories
    
    @property
    def carbs_today(self):
        carbs = 0
        for item in self.daily_food_items:
            carbs += item.food.carbs
        return carbs

    @property
    def fats_today(self):
        fats = 0
        for item in self.daily_food_items:
            fats += item.food.fats
        return fats

    @property
    def protein_today(self):
        protein = 0
        for item in self.daily_food_items:
            protein += item.food.protein
        return protein
    
    @property
    def calories_left_in_goal(self):
        if self.calorie_goal is None:
            return "You do not have a calorie goal!"
        return self.calorie_goal - self.calories_today

    def __str__(self):
        if self.user.first_name != "" or self.user.last_name != "":
            return f"{self.user.first_name} {self.user.last_name}"
        return f"username: {self.user.username}"


class UserFoodStorage(models.Model):
    date = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name="food_storage")
    food = models.ForeignKey(FoodItem,
                             on_delete=models.CASCADE,
                             related_name="food_storage",
                             null=True)

    def __str__(self):
        return f"Storage of user {self.user.__str__()} for {self.date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_delete, sender=Profile)
def delete_user_account(sender, instance, **kwargs):
    try:
        instance.user
    except Profile.DoesNotExist:
        pass
    else:
        instance.user.delete()

