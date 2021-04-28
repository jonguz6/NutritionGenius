from django import forms
from django.contrib.auth.models import User

from profiles.models import Profile, FoodItem


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ("weight", "height", "calorie_goal")


class FoodItemForm(forms.ModelForm):

    class Meta:
        model = FoodItem
        fields = ("ingredient", "quantity", "profile")
