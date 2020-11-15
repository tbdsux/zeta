from django.urls import path

from .views import others as views
from .views.collections import (
    CollectionsView,
    CollectionsPageView,
    CollectionsUpdateView,
    CollectionsDeleteView,
    CollectionsFindItemView,
    CollectionsRemoveItemView,
)
from .views.browse import BrowseView, BrowseResultsView
from .views.account import AccountSettingsView, ChangePasswordView, Account_Settings
from .views.index import IndexDashboardView

urlpatterns = [
    path("", IndexDashboardView.as_view(), name="dash"),
    # collections view
    path("collections/", CollectionsView.as_view(), name="collections"),
    path(
        "collections/<slug:slug>/",
        CollectionsPageView.as_view(),
        name="collections-page",
    ),
    path(
        "collections/<slug:slug>/update",
        CollectionsUpdateView.as_view(),
        name="collections-update",
    ),
    path(
        "collections/<slug:slug>/delete",
        CollectionsDeleteView.as_view(),
        name="collections-delete",
    ),
    path(
        "collections/<slug:slug>/add/find/<str:type>/<str:query>",
        CollectionsFindItemView.as_view(),
        name="collections-add-item",
    ),
    path(
        "collections/<slug:slug>/remove/<uuid:stuff_id>",
        CollectionsRemoveItemView.as_view(),
        name="collections-remove-item",
    ),
    # end collections view
    path("browse/", BrowseView.as_view(), name="browse"),
    path("browse/q/<str:query>", BrowseResultsView.as_view()),
    path("logout/", views.Logout, name="logout"),
    path("account/", Account_Settings, name="account"),
    path(
        "account/password/update", ChangePasswordView.as_view(), name="account-password"
    ),
]
