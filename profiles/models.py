from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from food_storage import models as food_models


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile",
                                primary_key=True)
    weight = models.FloatField()
    height = models.IntegerField()

    def __str__(self):
        if self.user.first_name != "" or self.user.last_name != "":
            return f"{self.user.first_name} {self.user.last_name}"
        return f"username: {self.user.username}"


class UserFoodStorage(models.Model):
    date = models.DateTimeField()
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="food_storage")
    food = models.ManyToManyField(food_models.FoodIngredient,
                                  related_name="food_storage")

    class Meta:
        unique_together = (('date', "user"),)

    def __str__(self):
        return f"Storage of user {self.user.__str__}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
