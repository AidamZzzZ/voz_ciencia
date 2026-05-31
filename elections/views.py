from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from .models import Campana
from .forms import CampanaForm, PlanchaFormSet

class AdminLoginView(LoginView):
    template_name = 'elections/admin_login.html'
    redirect_authenticated_user = True

class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'elections/admin_dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['campanas'] = Campana.objects.all().order_by('-fecha_inicio')
        return context

class CampanaCreateView(LoginRequiredMixin, CreateView):
    model = Campana
    form_class = CampanaForm
    template_name = 'elections/campana_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['planchas'] = PlanchaFormSet(self.request.POST, self.request.FILES)
        else:
            data['planchas'] = PlanchaFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        planchas = context['planchas']
        if planchas.is_valid():
            self.object = form.save()
            planchas.instance = self.object
            planchas.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CampanaUpdateView(LoginRequiredMixin, UpdateView):
    model = Campana
    form_class = CampanaForm
    template_name = 'elections/campana_form.html'
    success_url = reverse_lazy('admin_dashboard')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['planchas'] = PlanchaFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['planchas'] = PlanchaFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        planchas = context['planchas']
        if planchas.is_valid():
            self.object = form.save()
            planchas.instance = self.object
            planchas.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class CampanaDeleteView(LoginRequiredMixin, DeleteView):
    model = Campana
    template_name = 'elections/campana_confirm_delete.html'
    success_url = reverse_lazy('admin_dashboard')

class CampanaResultadosView(LoginRequiredMixin, DetailView):
    model = Campana
    template_name = 'elections/campana_resultados.html'
    context_object_name = 'campana'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campana = self.object
        
        planchas = campana.planchas.all()
        nombres_planchas = [p.nombre for p in planchas]
        votos_planchas = [p.votos_recibidos for p in planchas]
        
        total_votos = sum(votos_planchas)
        total_visitas = campana.votantes.count()
        
        porcentaje_participacion = 0
        if total_visitas > 0:
            porcentaje_participacion = round((total_votos / total_visitas) * 100, 1)
            
        context['total_votos'] = total_votos
        context['total_visitas'] = total_visitas
        context['porcentaje_participacion'] = porcentaje_participacion
        
        context['chart_labels'] = json.dumps(nombres_planchas)
        context['chart_data'] = json.dumps(votos_planchas)
        
        return context



