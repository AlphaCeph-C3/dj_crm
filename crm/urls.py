from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.LeadListView.as_view(), name="home"),
    path("create/", views.LeadCreateView.as_view(), name="lead-create"),
    path("update/<int:pk>/", views.LeadUpdateView.as_view(), name="lead-update"),
    path("delete/<int:pk>/", views.LeadDeleteView.as_view(), name="lead-delete"),
    path("detail/<int:pk>/", views.LeadDetailView.as_view(), name="lead-detail"),
    path(
        "assign-agent/<int:pk>/", views.AssignAgentView.as_view(), name="agent-assign"
    ),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "categories/<int:pk>/update/",
        views.LeadCategoryUpdateView.as_view(),
        name="lead-category-update",
    ),
    path(
        "create/category/", views.CategoryCreateView.as_view(), name="category-create"
    ),
    path(
        "update/<int:pk>/category/",
        views.CategoryUpdateView.as_view(),
        name="category-update",
    ),
    path(
        "delete/<int:pk>/category",
        views.CategoryDeleteView.as_view(),
        name="category-delete",
    ),
]
