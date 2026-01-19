from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
import json

class IndexView(TemplateView):
    template_name = 'index.html'

class SalaView(TemplateView):
    template_name = 'sala.html'

    def get_context_data(self, **kwargs):
        context = super(SalaView, self).get_context_data(**kwargs)
        nome_sala = self.kwargs['nome_sala']
        # Passa o nome da sala para o template em formato JSON seguro
        context['nome_sala_json'] = mark_safe(json.dumps(nome_sala))
        return context