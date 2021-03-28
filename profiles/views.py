import django.views.generic as views
from django.shortcuts import render
from django.urls import reverse_lazy

from profiles import models
from profiles.forms import ProfileForm


class ProfileCreateView(views.CreateView):
    model = models.Profile
    form_class = ProfileForm
    template_name = "Profile/profile-create.html"
    success_url = reverse_lazy('food_storage:category-list')


class ProfileListView(views.ListView):
    model = models.Profile
    template_name = "Profile/profile-list.html"


class ProfileDetailView(views.DetailView):
    model = models.Profile
    template_name = "Profile/profile-detail.html"


class ProfileUpdateView(views.UpdateView):
    model = models.Profile
    form_class = ProfileForm
    template_name = "Profile/profile-update.html"
    success_url = reverse_lazy('food_storage:category-list')


class ProfileDeleteView(views.DeleteView):
    model = models.Profile
    template_name = "Profile/profile-delete.html"
    success_url = reverse_lazy('food_storage:category-list')


def index(request):
    return render(
        request, template_name="profile-index.html"
    )