from django.urls import path

from .views import others as views
from .views.collections import CollectionsView
from .views.browse import BrowseView
from .views.account import AccountSettingsView

urlpatterns = [
    path("", views.index, name="dash"),
    path("collections/", CollectionsView.as_view(), name="collections"),
    path("browse/", BrowseView.as_view(), name="browse"),
    path("logout/", views.Logout, name="logout"),
    path("account/", AccountSettingsView.as_view(), name="profile"),
]
