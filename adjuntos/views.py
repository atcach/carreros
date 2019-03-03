from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import UpdateView
from django.db.models import Q
from elecciones.views import StaffOnlyMixing
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from .models import Attachment
from .forms import AsignarMesaForm


WAITING_FOR = 2   # 3 minutos


@staff_member_required
def elegir_adjunto(request):
    now = timezone.now()
    desde = now - timedelta(minutes=WAITING_FOR)

    # se eligen actas que nunca se intentaron cargar o que se asignaron a
    # hace más de 3 minutos
    attachments = Attachment.objects.filter(
        Q(problema__isnull=True, mesa__isnull=True),
        Q(taken__isnull=True) | Q(taken__lt=desde)
    ).order_by('?')
    if attachments.exists():
        a = attachments[0]
        # se marca el adjunto
        a.taken = now
        a.save(update_fields=['taken'])
        return redirect('asignar-mesa', attachment_id=a.id)

    return render(request, 'adjuntos/sin-actas.html')



class AsignarMesaAdjunto(StaffOnlyMixing, UpdateView):
    form_class = AsignarMesaForm
    template_name = "adjuntos/asignar-mesa.html"
    pk_url_kwarg = 'attachment_id'
    model = Attachment

    def get_success_url(self):
        return reverse('elegir-adjunto')

    def get_context_data(self, **kwargs):
        #import ipdb; ipdb.set_trace()
        context = super().get_context_data(**kwargs)
        context['attachment'] = self.object
        context['button_tabindex'] = 2
        return context

    def form_valid(self, form):
        form.save()
        # self.instance.mesa = form.cleaned_data['mesa']
        # self.attachment.save(update_fields=['mesa'])
        return super().form_valid(form)

