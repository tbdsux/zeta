from django.urls import path

from .views import others as views
from .views.collections import CollectionsView, CollectionsPageView
from .views.browse import BrowseView, BrowseResultsView
from .views.account import AccountSettingsView

urlpatterns = [
    path("", views.index, name="dash"),
    path("collections/", CollectionsView.as_view(), name="collections"),
    path("collections/<slug:slug>/", CollectionsPageView.as_view()),
    path("browse/", BrowseView.as_view(), name="browse"),
    path("browse/q/<str:query>", BrowseResultsView.as_view()),
    path("logout/", views.Logout, name="logout"),
    path("account/", AccountSettingsView.as_view(), name="account"),
]
