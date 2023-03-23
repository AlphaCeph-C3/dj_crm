# from django.contrib.auth.mixins import LoginRequiredMixin
import random

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.views import generic

from crm.models import Agent

from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin

# Create your views here.
User = get_user_model()


class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    template_name = "agents/agent_list.html"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 1000000)}")
        user.save()
        Agent.objects.create(user=user, organization=self.request.user.userprofile)
        send_mail(
            subject="You are invited to be an agent",
            message="You were added as an agent on DJCRM. Please come login and start working",
            from_email="test@user.com",
            recipient_list=[user.email],
        )
        # agent.organization = self.request.user.userprofile
        # agent.save()
        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)


class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "agents/agent_update.html"
    context_object_name = "agent"
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse("agents:agent-list")

    def get_queryset(self):
        organization = self.request.user.userprofile
        qs = Agent.objects.filter(organization=organization)
        return qs

    # since we are using a different model in form we need to send the user attribute of the agent model as the instance to update the user details
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs["instance"] = kwargs["instance"].user
        return kwargs


class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        organization = self.request.user.userprofile
        return Agent.objects.filter(organization=organization)

    def get_success_url(self):
        return reverse("agents:agent-list")
