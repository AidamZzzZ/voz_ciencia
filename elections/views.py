from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import qrcode
import base64
from io import BytesIO
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from django.db import transaction
from django.utils import timezone
import uuid
from .models import Campana, Plancha, Votante, AuditoriaVoto
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
        total_censo = 1800
        
        porcentaje_participacion = round((total_votos / total_censo) * 100, 1)
            
        context['total_votos'] = total_votos
        context['total_visitas'] = total_censo
        context['porcentaje_participacion'] = porcentaje_participacion
        
        context['chart_labels'] = json.dumps(nombres_planchas)
        context['chart_data'] = json.dumps(votos_planchas)
        
        auditorias = AuditoriaVoto.objects.filter(campana=campana).order_by('-fecha_emision')[:15]
        context['auditorias'] = auditorias
        
        return context

class CampanaVotacionView(DetailView):
    model = Campana
    template_name = 'elections/campana_votacion.html'
    context_object_name = 'campana'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.session.session_key:
            self.request.session.create()
            
        session_key = self.request.session.session_key
        ya_voto = Votante.objects.filter(campana=self.object, token_sesion=session_key, ya_voto=True).exists()
        
        comprobante = self.request.session.get(f'comprobante_{self.object.id}')
        
        context['ya_voto'] = ya_voto
        context['comprobante'] = comprobante
        return context

class EmitirVotoView(View):
    def post(self, request, pk):
        if not request.session.session_key:
            request.session.create()
            
        session_key = request.session.session_key
        plancha_id = request.POST.get('plancha_id')
        
        if not plancha_id:
            return redirect('campana_votar', pk=pk)
            
        with transaction.atomic():
            campana = Campana.objects.get(id=pk)
            if not campana.esta_activa:
                return redirect('campana_votar', pk=pk)
                
            votante, created = Votante.objects.select_for_update().get_or_create(
                token_sesion=session_key, 
                campana=campana
            )
            
            if not votante.ya_voto:
                try:
                    plancha = Plancha.objects.select_for_update().get(id=plancha_id, campana=campana)
                    plancha.votos_recibidos += 1
                    plancha.save()
                    
                    votante.ya_voto = True
                    votante.fecha_voto = timezone.now()
                    votante.save()
                    
                    comprobante_hash = str(uuid.uuid4())
                    AuditoriaVoto.objects.create(
                        comprobante=comprobante_hash,
                        campana=campana
                    )
                    request.session[f'comprobante_{campana.id}'] = comprobante_hash
                except Plancha.DoesNotExist:
                    pass
                    
        return redirect('campana_votar', pk=pk)

class CampanaQRView(LoginRequiredMixin, DetailView):
    model = Campana
    template_name = 'elections/campana_qr.html'
    context_object_name = 'campana'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        campana = self.object
        
        url_votacion = self.request.build_absolute_uri(reverse('campana_votar', kwargs={'pk': campana.id}))
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url_votacion)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        context['qr_code_base64'] = qr_base64
        return context
