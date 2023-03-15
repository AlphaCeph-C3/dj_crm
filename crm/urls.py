from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("", views.lead_list, name="home"),
    path("create/", views.lead_create, name="lead-create"),
    path("update/<int:pk>/", views.lead_update, name="lead-update"),
    path("delete/<int:pk>/", views.lead_delete, name="lead-delete"),
    path("detail/<int:pk>/", views.lead_detail, name="lead-detail"),
]
