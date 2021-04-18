import django.views.generic as views
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy

from food_storage import models


class FoodCategoryCreateView(PermissionRequiredMixin, views.CreateView):
    permission_required = ('food_storage.add_food_category', )
    model = models.FoodCategory
    fields = "__all__"
    template_name = "FoodCategory/category-create.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodCategoryListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('food_storage.view_food_category', )
    model = models.FoodCategory
    template_name = "FoodCategory/category-list.html"


class FoodCategoryDetailView(PermissionRequiredMixin, views.DetailView):
    permission_required = ('food_storage.view_food_category', )
    model = models.FoodCategory
    template_name = "FoodCategory/category-detail.html"


class FoodCategoryUpdateView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('food_storage.update_food_category', )
    model = models.FoodCategory
    fields = "__all__"
    template_name = "FoodCategory/category-update.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodCategoryDeleteView(PermissionRequiredMixin, views.DeleteView):
    permission_required = ('food_storage.delete_food_category', )
    model = models.FoodCategory
    template_name = "FoodCategory/category-delete.html"
    success_url = reverse_lazy('food_storage:category-list')


class FoodIngredientCreateView(PermissionRequiredMixin, views.CreateView):
    permission_required = ('food_storage.add_food_ingredient', )
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

    def post(self, request, *args, **kwargs):
        post = request.POST.copy()
        if post.get('category') is None:
            post['category'] = self.kwargs.get('cat_pk')
        request.POST = post
        return super().post(request, *args, **kwargs)


class FoodIngredientListView(PermissionRequiredMixin, views.ListView):
    permission_required = ('food_storage.view_food_ingredient', )
    model = models.FoodIngredient
    template_name = "FoodIngredient/ingredient-list.html"

    def get_queryset(self):
        category = self.kwargs.get('cat_pk')
        if category is None:
            return super().get_queryset()
        return models.FoodIngredient.objects.filter(category=category)


class FoodIngredientDetailView(PermissionRequiredMixin, views.DetailView):
    permission_required = ('food_storage.view_food_ingredient', )
    model = models.FoodIngredient
    template_name = "FoodIngredient/ingredient-detail.html"


class FoodIngredientUpdateView(PermissionRequiredMixin, views.UpdateView):
    permission_required = ('food_storage.update_food_ingredient', )
    model = models.FoodIngredient
    fields = "__all__"
    template_name = "FoodIngredient/ingredient-update.html"
    success_url = reverse_lazy('food_storage:ingredient-list')


class FoodIngredientDeleteView(PermissionRequiredMixin, views.DeleteView):
    permission_required = ('food_storage.delete_food_ingredient', )
    model = models.FoodIngredient
    template_name = "FoodIngredient/ingredient-delete.html"
    success_url = reverse_lazy('food_storage:ingredient-list')


@permission_required('food_storage.view_food_ingredient')
def index(request):
    return render(
        request, template_name="food_storage-index.html"
    )


