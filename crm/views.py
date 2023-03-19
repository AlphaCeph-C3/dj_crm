from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from agents.mixins import OrganizerAndLoginRequiredMixin

from .forms import CustomUserCreationForm, LeadModelForm
from .models import Lead

# Create your views here.


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse("login")


class LandingPageView(TemplateView):
    template_name = "crm/landing.html"


class LeadListView(LoginRequiredMixin, ListView):
    template_name = "crm/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadDetailView(LoginRequiredMixin, DetailView):
    template_name = "crm/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # filter for the agent logged in
            queryset = queryset.filter(agent__user=user)
        return queryset


class LeadCreateView(OrganizerAndLoginRequiredMixin, CreateView):
    """Create a CBV with model form so that it is saved into the database directly when submitted through the webpage and deal with sending emails to either client leads or to created agents.

    Args:
        CreateView (generic views): django builtin view for creating database rows which is inherited by the current view.

    Returns:
        HTTPResponse: An HTTPResponse which renders a template on the browser.
    """

    template_name = "crm/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("crm:home")

    def form_valid(self, form):
        # TODO: send email
        send_mail(
            subject="A Lead has been created.",
            message="Go to the site to see the new lead.",
            from_email="test@test.com",
            recipient_list=["test2@test.com"],
        )
        return super(LeadCreateView, self).form_valid(form)


class LeadUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):
    template_name = "crm/lead_update.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("crm:home")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset


class LeadDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = "crm/lead_delete.html"

    def get_success_url(self) -> str:
        return reverse("crm:home")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        queryset = Lead.objects.filter(organization=user.userprofile)
        return queryset
