from django.shortcuts import get_object_or_404, redirect, render
from django.forms.models import model_to_dict
from .forms import LeadForm, LeadModelForm
from .models import Agent, Lead

# Create your views here.


def lead_list(request):
    leads = Lead.objects.all()
    context = {"leads": leads}
    return render(request, "crm/lead_list.html", context=context)


def lead_detail(request, pk):
    lead = get_object_or_404(Lead, pk=pk)
    context = {"lead": lead}
    return render(request, "crm/lead_detail.html", context)


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


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("crm:home")


# def lead_update(request, pk):
#     lead = get_object_or_404(Lead, pk=pk)
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data.get("first_name")
#             last_name = form.cleaned_data.get("last_name")
#             age = form.cleaned_data.get("age")
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("crm:home")
#     else:
#         lead_data = {"first_name": lead.first_name, "last_name": lead.last_name, "age": lead.age}
#         print(model_to_dict(lead))
#         form = LeadForm(initial=lead_data)
#     context = {
#         "lead": lead,
#         "form": form,
#     }
#     return render(request, "crm/lead_update.html", context)


# def lead_create(request):
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data.get("first_name")
#             last_name = form.cleaned_data.get("last_name")
#             age = form.cleaned_data.get("age")
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name, last_name=last_name, age=age, agent=agent
#             )
#             return redirect("crm:home")
#     else:
#         form = LeadForm()
#     context = {
#         "form": form,
#     }
#     return render(request, "crm/lead_create.html", context)
