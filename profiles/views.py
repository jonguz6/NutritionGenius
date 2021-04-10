import django.views.generic as views
from django.shortcuts import render
from django.urls import reverse_lazy

from profiles import models, forms


class ProfileCreateView(views.CreateView):
    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "Profile/profile-create.html"
    success_url = reverse_lazy('profiles:profile-list')


class ProfileListView(views.ListView):
    model = models.Profile
    template_name = "Profile/profile-list.html"


class ProfileDetailView(views.DetailView):
    model = models.Profile
    template_name = "Profile/profile-detail.html"


class ProfileUpdateView(views.UpdateView):
    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "Profile/profile-update.html"
    success_url = reverse_lazy('profiles:profile-list')


class ProfileDeleteView(views.DeleteView):
    model = models.Profile
    template_name = "Profile/profile-delete.html"
    success_url = reverse_lazy('profiles:profile-list')


class FoodItemCreateView(views.CreateView):
    model = models.FoodItem
    form_class = forms.FoodItemForm
    template_name = "FoodItem/food_item-create.html"
    success_url = reverse_lazy('profiles:food_item-list')
    

class FoodItemListView(views.ListView):
    model = models.FoodItem
    template_name = "FoodItem/food_item-list.html"


class FoodItemDetailView(views.DetailView):
    model = models.FoodItem
    template_name = "FoodItem/food_item-detail.html"


class FoodItemUpdateView(views.UpdateView):
    model = models.FoodItem
    form_class = forms.FoodItemForm
    template_name = "FoodItem/food_item-update.html"
    success_url = reverse_lazy('profiles:food_item-list')


class FoodItemDeleteView(views.DeleteView):
    model = models.FoodItem
    template_name = "FoodItem/food_item-delete.html"
    success_url = reverse_lazy('profiles:food_item-list')


class UserFoodStorageCreateView(views.CreateView):
    model = models.UserFoodStorage
    form_class = forms.UserFoodStorageForm
    template_name = "UserFoodStorage/food_storage-create.html"
    success_url = reverse_lazy('profiles:food_storage-list')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()

        profile_id = self.kwargs.get('prof_id')
        if profile_id:
            profile = models.Profile.objects.get(pk=profile_id)
            form_kwargs['initial'].update({'user': profile})

        food_id = self.kwargs.get('food_id')
        if food_id:
            food = models.FoodItem.objects.get(id=food_id)
            form_kwargs['initial'].update({'food': food})

        return form_kwargs


class UserFoodStorageListView(views.ListView):
    model = models.UserFoodStorage
    template_name = "UserFoodStorage/food_storage-list.html"


class UserFoodStorageDetailView(views.DetailView):
    model = models.UserFoodStorage
    template_name = "UserFoodStorage/food_storage-detail.html"


class UserFoodStorageUpdateView(views.UpdateView):
    model = models.UserFoodStorage
    form_class = forms.UserFoodStorageForm
    template_name = "UserFoodStorage/food_storage-update.html"
    success_url = reverse_lazy('profiles:food_storage-list')


class UserFoodStorageDeleteView(views.DeleteView):
    model = models.UserFoodStorage
    template_name = "UserFoodStorage/food_storage-delete.html"
    success_url = reverse_lazy('profiles:food_storage-list')


def index(request):
    return render(
        request, template_name="profile-index.html"
    )
