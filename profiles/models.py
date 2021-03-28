from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="profile",
                                primary_key=True)
    weight = models.FloatField(blank=True, null=True)
    height = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.user.first_name or self.user.last_name != "":
            return f"{self.user.first_name} {self.user.last_name}"
        return f"username: {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
