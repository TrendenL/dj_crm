from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead, Agent
from agents.mixins import OrganizerAndLoginRequiredMixin
from .form import LeadForm, CustomUserCreationForm


class SignupView(generic.CreateView):
    template_name="registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing_page.html"

def landing_page(request):
    return render(request, "landing_page.html")

class LeadListView(LoginRequiredMixin ,generic.ListView):
    template_name = "leads/lead_list.html"

    def get_queryset(self):
        user = self.request.user
        # Inital queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # Filter for the agent
            queryset = queryset.filter(agent__user=user)

        return queryset

    context_object_name = "leads"

def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads": leads
    }
    return render(request, "leads/lead_list.html", context)

class LeadDetailView(LoginRequiredMixin ,generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # Inital queryset of leads for the entire organization
        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=user.agent.organization)
            # Filter for the agent
            queryset = queryset.filter(agent__user=user)

        return queryset

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

class LeadCreatView(OrganizerAndLoginRequiredMixin ,generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadForm

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        send_mail(
            subject="A lead has been created",
            message="Go to site to see the new lead",
            from_email="test@test.com",
            recipient_list="test2@test.com"
        )
        return super(LeadCreatView, self).form_valid(form)

def lead_create(request):
    form = LeadForm()
    if request.method == "POST":
        form = LeadForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)

class LeadUpdateView(OrganizerAndLoginRequiredMixin ,generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadForm

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

    def get_success_url(self):
        return reverse("leads:lead-list")

def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadForm(instance=lead)

    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    
    context = {
        "form": form,
        "lead": lead
    }
    return render(request, "leads/lead_update.html", context)

class LeadDeleteView(OrganizerAndLoginRequiredMixin ,generic.DeleteView):
    template_name = "leads/lead_delete.html"

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        return Lead.objects.filter(organization=user.userprofile)

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")