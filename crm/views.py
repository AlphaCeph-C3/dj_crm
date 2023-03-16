from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from .forms import LeadModelForm
from .models import Lead

# Create your views here.


class LandingPageView(TemplateView):
    template_name = "crm/landing.html"


def landing_page(request):
    context = {}
    return render(request, "crm/landing.html", context=context)


class LeadListView(ListView):
    template_name = "crm/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"


def lead_list(request):
    leads = Lead.objects.all()
    context = {"leads": leads}
    return render(request, "crm/lead_list.html", context=context)


class LeadDetailView(DetailView):
    template_name = "crm/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"


def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    context = {"lead": lead}
    return render(request, "crm/lead_detail.html", context)


class LeadCreateView(CreateView):
    template_name = "crm/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("crm:home")


def lead_create(request):
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("crm:home")
    else:
        form = LeadModelForm()
    context = {
        "form": form,
    }
    return render(request, "crm/lead_create.html", context)


class LeadUpdateView(UpdateView):
    template_name = "crm/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("crm:home")


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("crm:home")
    else:
        form = LeadModelForm(instance=lead)
    context = {
        "lead": lead,
        "form": form,
    }
    return render(request, "crm/lead_update.html", context)


class LeadDeleteView(DeleteView):
    template_name = "crm/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self) -> str:
        return reverse("crm:home")


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("crm:home")
