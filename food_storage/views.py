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
    fields = "__all__"
    template_name = "FoodCategory/category-update.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodCategoryDeleteView(views.DeleteView):
    model = models.FoodCategory
    template_name = "FoodCategory/category-delete.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodIngredientCreateView(views.CreateView):
    model = models.FoodIngredient
    fields = "__all__"
    template_name = "FoodIngredient/ingredient-create.html"
    success_url = reverse_lazy('food_storage:ingredient-list')

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        category = self.kwargs.get('cat_pk')
        if category is None:
            return form_kwargs
        form_kwargs['initial'] = {'category': models.FoodCategory.objects.get(id=category)}
        return form_kwargs


class FoodIngredientListView(views.ListView):
    model = models.FoodIngredient
    template_name = "FoodIngredient/ingredient-list.html"


class FoodIngredientDetailView(views.DetailView):
    model = models.FoodIngredient
    template_name = "FoodIngredient/ingredient-detail.html"


class FoodIngredientUpdateView(views.UpdateView):
    model = models.FoodIngredient
    fields = "__all__"
    template_name = "FoodIngredient/ingredient-update.html"
    success_url = reverse_lazy('food_storage:ingredient-list')


class FoodIngredientDeleteView(views.DeleteView):
    model = models.FoodIngredient
    template_name = "FoodIngredient/ingredient-delete.html"
    success_url = reverse_lazy('food_storage:ingredient-list')


def index(request):
    return render(
        request, template_name="food_storage-index.html"
    )


