from django.urls import path

from food_storage import views

app_name = "food_storage"
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
    
]
