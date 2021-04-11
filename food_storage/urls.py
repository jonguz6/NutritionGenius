from django.urls import path

from food_storage import views

urlpatterns = [
    path('', views.index, name="index"),
    
    path('category-create/', 
         views.FoodCategoryCreateView.as_view(), 
         name="category-create"),
    path('category-list/',
         views.FoodCategoryListView.as_view(),
         name="category-list"),
    path('category-detail/<pk>/',
         views.FoodCategoryDetailView.as_view(), 
         name="category-detail"),
    path('category-update/<pk>/',
         views.FoodCategoryUpdateView.as_view(), 
         name="category-update"),
    path('category-delete/<pk>/',
         views.FoodCategoryDeleteView.as_view(), 
         name="category-delete"),
    
    path('ingredient-create/', 
         views.FoodIngredientCreateView.as_view(), 
         name="ingredient-create"),
    path('ingredient-create/cat/<cat_pk>',
         views.FoodIngredientCreateView.as_view(),
         name="ingredient-create-w-cat"),
    path('ingredient-list/',
         views.FoodIngredientListView.as_view(),
         name="ingredient-list"),
    path('ingredient-detail/<pk>/',
         views.FoodIngredientDetailView.as_view(), 
         name="ingredient-detail"),
    path('ingredient-update/<pk>/',
         views.FoodIngredientUpdateView.as_view(), 
         name="ingredient-update"),
    path('ingredient-delete/<pk>/',
         views.FoodIngredientDeleteView.as_view(), 
         name="ingredient-delete"),
    
]
