from django.urls import path

from profiles import views

app_name = "profiles"
urlpatterns = [
    path('', views.index, name="index"),

    path('profile-create/',
         views.ProfileCreateView.as_view(),
         name="profile-create"),
    path('profile-list/',
         views.ProfileListView.as_view(),
         name="profile-list"),
    path('profile-detail/<pk>/',
         views.ProfileDetailView.as_view(),
         name="profile-detail"),
    path('profile-update/<pk>/',
         views.ProfileUpdateView.as_view(),
         name="profile-update"),
    path('profile-delete/<pk>/',
         views.ProfileDeleteView.as_view(),
         name="profile-delete"),
]