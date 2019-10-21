from django.views.generic.base import TemplateView

class FrontendView(TemplateView):
    template_name = "backend/index.html"