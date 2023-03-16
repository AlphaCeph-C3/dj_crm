from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.LeadListView.as_view(), name="home"),
    path("create/", views.LeadCreateView.as_view(), name="lead-create"),
    path("update/<int:pk>/", views.LeadUpdateView.as_view(), name="lead-update"),
    path("delete/<int:pk>/", views.LeadDeleteView.as_view(), name="lead-delete"),
    path("detail/<int:pk>/", views.LeadDetailView.as_view(), name="lead-detail"),
]
