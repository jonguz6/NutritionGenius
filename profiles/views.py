from datetime import date

import django.views.generic as views
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from profiles import models, forms


def check_user_has_access(instance, request):
    user = request.user
    profile = models.Profile.objects.get(user=user)
    checked_object = instance.get_object()
    if profile == checked_object.user:
        return True
    return False


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


class FoodStorageForUserListView(views.ListView):
    model = models.UserFoodStorage
    template_name = "UserFoodStorage/food_storage-user-list.html"

    def get_queryset(self):
        pk = self.kwargs.get('prof_id')
        return models.UserFoodStorage.objects.filter(user=pk)


class FoodStorageForTodayListView(views.ListView):
    model = models.UserFoodStorage
    template_name = "UserFoodStorage/food_storage-user-list.html"

    def get_queryset(self):
        pk = self.kwargs.get('prof_id')
        today = date.today()
        return models.UserFoodStorage.objects.filter(user=pk, date=today)


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

###############
# User Views #
##############


class SelfProfileDetailView(LoginRequiredMixin, views.DetailView):
    model = models.Profile
    template_name = "Current-User/profile-detail.html"

    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user=user)


class SelfProfileUpdateView(LoginRequiredMixin, views.UpdateView):
    model = models.Profile
    template_name = "Current-User/profile-update.html"
    success_url = reverse_lazy('profiles:user-profile')
    form_class = forms.ProfileForm

    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user=user)


class SelfProfileDeleteView(LoginRequiredMixin, views.DeleteView):
    model = models.Profile
    template_name = "Current-User/profile-delete.html"
    success_url = reverse_lazy('profiles:profile-list')

    def get_object(self):
        user = self.request.user
        return models.Profile.objects.get(user=user)


class FoodStorageForCurrentUserDetailView(LoginRequiredMixin, views.DetailView):
    model = models.UserFoodStorage
    template_name = "Current-User/profile-food-detail.html"

    def get(self, request, *args, **kwargs):
        if check_user_has_access(self, request):
            return super().get(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view this item!")
        return redirect(request.META.get('HTTP_REFERER') or reverse_lazy('profiles:user-profile'))


class FoodStorageForCurrentUserUpdateView(LoginRequiredMixin, views.UpdateView):
    model = models.UserFoodStorage
    template_name = "Current-User/profile-food-update.html"
    form = forms.UserFoodStorageForm

    def get(self, request, *args, **kwargs):
        if check_user_has_access(self, request):
            return super().get(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view this item!")
        return redirect(request.META.get('HTTP_REFERER') or reverse_lazy('profiles:user-profile'))

    def get_success_url(self):
        return reverse_lazy("profiles:user-food-detail",
                            kwargs={'pk': self.object.id})


class FoodStorageForCurrentUserDeleteView(LoginRequiredMixin, views.UpdateView):
    model = models.UserFoodStorage
    template_name = "Current-User/profile-food-update.html"
    success_url = reverse_lazy('profiles:user-food_storage')

    def get(self, request, *args, **kwargs):
        if check_user_has_access(self, request):
            return super().get(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view this item!")
        return redirect(request.META.get('HTTP_REFERER') or reverse_lazy('profiles:user-profile'))


class FoodStorageForCurrentUserListView(LoginRequiredMixin, views.ListView):
    model = models.UserFoodStorage
    template_name = "Current-User/profile-food-storage.html"

    def get_queryset(self):
        user = self.request.user
        profile = models.Profile.objects.get(user=user)
        return models.UserFoodStorage.objects.filter(user=profile)


class TodayFoodStorageForCurrentUserListView(LoginRequiredMixin, views.ListView):
    model = models.UserFoodStorage
    template_name = "Current-User/profile-food-storage.html"

    def get_queryset(self):
        user = self.request.user
        today = date.today()
        profile = models.Profile.objects.get(user=user)
        return models.UserFoodStorage.objects.filter(user=profile, date=today)


@login_required(login_url=reverse_lazy('login'))
def user_food_storage_create_view(request):
    food_storage_form_set2 = modelformset_factory(models.FoodItem, fields=('ingredient', 'quantity'), extra=5)
    user = request.user
    profile = models.Profile.objects.get(user=user)
    formset2 = food_storage_form_set2(queryset=models.FoodItem.objects.none())
    context = {'formset1': formset2, 'pk': user}
    if request.method == "POST":
        formset = food_storage_form_set2(request.POST)
        if formset.is_valid():
            for f in formset:
                form_data = f.cleaned_data
                item_ingredient = form_data.get('ingredient')
                item_quantity = form_data.get('quantity')
                try:
                    item = models.FoodItem.objects.create(ingredient=item_ingredient, quantity=item_quantity)
                except IntegrityError:
                    pass
                else:
                    item.save()
                    try:
                        storage = models.UserFoodStorage.objects.create(user=profile, food=item)
                    except IntegrityError:
                        pass
                    else:
                        storage.save()
                        messages.success(request, "Your meal has been saved successfully!")
        else:
            messages.error(request, "Save unsuccessful, make sure you entered a meal!")
    return render(
        request, "Current-User/profile-form.html", context
    )


def index(request):
    return render(
        request, template_name="profile-index.html"
    )
