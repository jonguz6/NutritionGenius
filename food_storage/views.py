import django.views.generic as views
from django.shortcuts import render

from food_storage import models


class FoodCategoryCreateView(views.CreateView):
    model = models.FoodCategory
    fields = "__all__"
    template_name = "FoodCategory/category-create.html"


class FoodCategoryListView(views.ListView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-list.html"


class FoodCategoryDetailView(views.DetailView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-detail.html"


class FoodCategoryUpdateView(views.UpdateView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-update.html"


class FoodCategoryDeleteView(views.DeleteView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-delete.html"


def index(request):
    return render(
        request, template_name="food_storage-index.html"
    )


