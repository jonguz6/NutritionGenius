import django.views.generic as views
from django.shortcuts import render
from django.urls import reverse_lazy

from food_storage import models


class FoodCategoryCreateView(views.CreateView):
    model = models.FoodCategory
    fields = "__all__"
    template_name = "FoodCategory/category-create.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodCategoryListView(views.ListView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-list.html"


class FoodCategoryDetailView(views.DetailView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-detail.html"


class FoodCategoryUpdateView(views.UpdateView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-update.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodCategoryDeleteView(views.DeleteView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-delete.html"
    success_url = reverse_lazy('food_storage:category-list')


def index(request):
    return render(
        request, template_name="food_storage-index.html"
    )


