from django.urls import path

from .views import (
    AgentCreateView,
    AgentDeleteView,
    AgentDetailView,
    AgentListView,
    AgentUpdateView,
)

app_name = "agents"

urlpatterns = [
    path("", AgentListView.as_view(), name="agent-list"),
    path("create/", AgentCreateView.as_view(), name="agent-create"),
    path("agent/update/<int:pk>/", AgentUpdateView.as_view(), name="agent-update"),
    path("agent/delete/<int:pk>/", AgentDeleteView.as_view(), name="agent-delete"),
    path("agent/detail/<int:pk>/", AgentDetailView.as_view(), name="agent-detail"),
]
