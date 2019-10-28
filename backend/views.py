from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.views import APIView
from rest_framework.response import Response


class FrontendView(LoginRequiredMixin, TemplateView):
    login_url = "/accounts/login/"
    template_name = "backend/index.html"


# noinspection PyMethodMayBeStatic
class LoginSuccessView(APIView):
    def get(self, request):
        content = {'username': request.user.username}
        return Response(content)


# noinspection PyMethodMayBeStatic
class LoginFailureView(APIView):
    def get(self, request):
        return Response("no good")
