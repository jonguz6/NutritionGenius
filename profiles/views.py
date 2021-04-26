from datetime import date

import django.views.generic as views
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import IntegrityError
from django.forms import modelformset_factory
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from profiles import models, forms


def check_user_has_access(instance, request):
    user = request.user
    profile = models.Profile.objects.get(user=user)
    checked_object = instance.get_object()
    if profile == checked_object.profile:
        return True
    return False


class ProfileCreateView(PermissionRequiredMixin, views.CreateView):
    permission_required = ('profiles.add_profile', )
    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "Profile/profile-create.html"
    success_url = reverse_lazy('profiles:profile-list')


class ProfileListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('profiles.view_profile', )
    model = models.Profile
    template_name = "Profile/profile-list.html"


class ProfileDetailView(PermissionRequiredMixin, views.DetailView):
    permission_required = ('profiles.view_profile', )
    model = models.Profile
    template_name = "Profile/profile-detail.html"


class ProfileUpdateView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('profiles.change_profile', )
    model = models.Profile
    form_class = forms.ProfileForm
    template_name = "Profile/profile-update.html"
    success_url = reverse_lazy('profiles:profile-list')


class ProfileDeleteView(PermissionRequiredMixin, views.DeleteView):
    permission_required = ('profiles.delete_profile', )
    model = models.Profile
    template_name = "Profile/profile-delete.html"
    success_url = reverse_lazy('profiles:profile-list')


class FoodItemCreateView(PermissionRequiredMixin, views.CreateView):
    permission_required = ('profiles.add_fooditem', )
    model = models.FoodItem
    form_class = forms.FoodItemForm
    template_name = "FoodItem/food_item-create.html"
    success_url = reverse_lazy('profiles:food_item-list')


class FoodItemListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('profiles.view_fooditem', )
    model = models.FoodItem
    template_name = "FoodItem/food_item-list.html"


class FoodItemDetailView(PermissionRequiredMixin, views.DetailView):
    permission_required = ('profiles.view_fooditem', )
    model = models.FoodItem
    template_name = "FoodItem/food_item-detail.html"


class FoodItemUpdateView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('profiles.change_fooditem', )
    model = models.FoodItem
    form_class = forms.FoodItemForm
    template_name = "FoodItem/food_item-update.html"
    success_url = reverse_lazy('profiles:food_item-list')


class FoodItemDeleteView(PermissionRequiredMixin, views.DeleteView):
    permission_required = ('profiles.delete_fooditem', )
    model = models.FoodItem
    template_name = "FoodItem/food_item-delete.html"
    success_url = reverse_lazy('profiles:food_item-list')


class FoodStorageForUserListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('profiles.view_fooditem', )
    model = models.FoodItem
    template_name = "UserFoodStorage/food_storage-user-list.html"

    def get_queryset(self):
        pk = self.kwargs.get('prof_id')
        return models.FoodItem.objects.filter(pk=pk)


class FoodStorageForTodayListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('profiles.view_fooditem', )
    model = models.FoodItem
    template_name = "UserFoodStorage/food_storage-user-list.html"

    def get_queryset(self):
        pk = self.kwargs.get('prof_id')
        today = date.today()
        return models.FoodItem.objects.filter(user=pk, date=today)
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
    model = models.FoodItem
    template_name = "Current-User/profile-food-detail.html"

    def get(self, request, *args, **kwargs):
        if check_user_has_access(self, request):
            return super().get(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view this item!", extra_tags='alert-danger')
        return redirect(request.META.get('HTTP_REFERER') or reverse_lazy('profiles:user-profile'))


class FoodStorageForCurrentUserUpdateView(LoginRequiredMixin, views.UpdateView):
    model = models.FoodItem
    template_name = "Current-User/profile-food-update.html"
    form_class = forms.FoodItemForm

    def get(self, request, *args, **kwargs):
        if check_user_has_access(self, request):
            return super().get(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view this item!", extra_tags='alert-danger')
        return redirect(request.META.get('HTTP_REFERER') or reverse_lazy('profiles:user-profile'))

    def get_success_url(self):
        return reverse_lazy("profiles:user-food-detail",
                            kwargs={'pk': self.object.id})


class FoodStorageForCurrentUserDeleteView(LoginRequiredMixin, views.DeleteView):
    model = models.FoodItem
    template_name = "Current-User/profile-food-delete.html"
    success_url = reverse_lazy('profiles:user-today-food_storage')

    def get(self, request, *args, **kwargs):
        if check_user_has_access(self, request):
            return super().get(request, *args, **kwargs)
        messages.error(request, "You do not have permission to view this item!", extra_tags='alert-danger')
        return redirect(request.META.get('HTTP_REFERER') or reverse_lazy('profiles:user-profile'))


class FoodStorageForCurrentUserListView(LoginRequiredMixin, views.ListView):
    model = models.FoodItem
    template_name = "Current-User/profile-food-storage.html"

    def get_queryset(self):
        user = self.request.user
        profile = models.Profile.objects.get(user=user)
        return models.FoodItem.objects.filter(profile=profile).order_by('-date')


class TodayFoodStorageForCurrentUserListView(LoginRequiredMixin, views.ListView):
    model = models.FoodItem
    template_name = "Current-User/profile-food-storage.html"

    def get_queryset(self):
        user = self.request.user
        today = date.today()
        profile = models.Profile.objects.get(user=user)
        return models.FoodItem.objects.filter(profile=profile, date=today).order_by('-date')


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
                    item = models.FoodItem.objects.create(ingredient=item_ingredient, quantity=item_quantity, profile=user.profile)
                except IntegrityError:
                    pass
                else:
                    item.save()

                    messages.success(request, "Your meal has been saved successfully!", extra_tags='alert-success')
        else:
            messages.error(request, "Save unsuccessful, make sure you entered a meal!", extra_tags='alert-danger')
    return render(
        request, "Current-User/profile-form.html", context
    )


@permission_required('profiles.view_profile')
def index(request):
    return render(
        request, template_name="profile-index.html"
    )
