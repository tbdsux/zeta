from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="dash"),
    path("collections/", views.collections, name="collections"),
    path("browse/", views.browse, name="browse"),
    path("logout/", views.Logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]
