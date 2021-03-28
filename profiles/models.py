from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from food_storage.models import FoodIngredient


class FoodItem(models.Model):
    ingredient = models.ForeignKey(FoodIngredient,
                                   related_name="food_items",
                                   on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = (('ingredient', "quantity"),)

    def __str__(self):
        return f"{self.ingredient.__str__} q: {self.quantity}"


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

    def __str__(self):
        if self.user.first_name != "" or self.user.last_name != "":
            return f"{self.user.first_name} {self.user.last_name}"
        return f"username: {self.user.username}"


class UserFoodStorage(models.Model):
    date = models.DateField(auto_created=True)
    user = models.ForeignKey(Profile,
                             on_delete=models.CASCADE,
                             related_name="food_storage")
    food = models.ForeignKey(FoodItem,
                             on_delete=models.CASCADE,
                             related_name="food_storage",
                             null=True)

    class Meta:
        unique_together = (('date', "user"),)

    def __str__(self):
        return f"Storage of user {self.user.__str__} for {self.date}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
