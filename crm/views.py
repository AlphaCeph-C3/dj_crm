from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    FormView,
    ListView,
    TemplateView,
    UpdateView,
)

from agents.mixins import OrganizerAndLoginRequiredMixin

from .forms import (
    AssignAgentForm,
    CategoryModelForm,
    CustomUserCreationForm,
    LeadCategoryUpdateForm,
    LeadModelForm,
)
from .models import Category, Lead

# Create your views here.


class SignupView(CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    # for authenticated users to return to the crm home page instead of going into the signup page
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("crm:home")
        return super(SignupView, self).get(request, *args, **kwargs)

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
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=False
            )
        else:
            queryset = Lead.objects.filter(
                organization=user.agent.organization, agent__isnull=False
            )
            # filter for the agent logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_context_data(self, **kwargs):
        user = self.request.user
        context = super(LeadListView, self).get_context_data(**kwargs)
        if user.is_organizer:
            queryset = Lead.objects.filter(
                organization=user.userprofile, agent__isnull=True
            )
            context.update(
                {
                    "unassigned_leads": queryset,
                }
            )
        return context


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
        lead = form.save(commit=False)
        lead.organization = self.request.user.userprofile
        lead.save()
        # TODO: send email
        send_mail(
            subject="A Lead has been created.",
            message="Go to the site to see the new lead.",
            from_email="test@test.com",
            recipient_list=["test2@test.com"],
        )
        messages.success(self.request, "You have successfully create a lead.")
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


class AssignAgentView(OrganizerAndLoginRequiredMixin, FormView):
    template_name = "crm/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({"request": self.request})
        return kwargs

    def get_success_url(self):
        return reverse("crm:home")

    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = "crm/category_list.html"
    context_object_name = "category_list"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
        context.update(
            {"unassigned_lead_count": queryset.filter(category__isnull=True).count()}
        )
        return context


class CategoryDetailView(LoginRequiredMixin, DetailView):
    template_name = "crm/category_detail.html"
    context_object_name = "category"

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # category = self.get_object()
    #     # qs = Lead.objects.filter(category=category)
    #     leads = self.get_object().leads.all()
    #     context.update({"leads": leads})
    #     return context


class LeadCategoryUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "crm/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("crm:lead-detail", kwargs={"pk": self.get_object().pk})


class CategoryCreateView(OrganizerAndLoginRequiredMixin, CreateView):

    template_name = "crm/category_create.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("crm:category-list")

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.userprofile
        category.save()
        return super(CategoryCreateView, self).form_valid(form)


class CategoryUpdateView(OrganizerAndLoginRequiredMixin, UpdateView):

    template_name = "crm/category_update.html"
    form_class = CategoryModelForm

    def get_success_url(self):
        return reverse("crm:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset


class CategoryDeleteView(OrganizerAndLoginRequiredMixin, DeleteView):
    template_name = "crm/category_delete.html"

    def get_success_url(self):
        return reverse("crm:category-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Category.objects.filter(organization=user.userprofile)
        else:
            queryset = Category.objects.filter(organization=user.agent.organization)

        return queryset
