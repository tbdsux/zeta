from django.urls import path

from . import views
from .views import CollectionsView

urlpatterns = [
    path("", views.index, name="dash"),
    path("collections/", CollectionsView.as_view(), name="collections"),
    path("browse/", views.browse, name="browse"),
    path("logout/", views.Logout, name="logout"),
    path("profile/", views.profile, name="profile"),
]
