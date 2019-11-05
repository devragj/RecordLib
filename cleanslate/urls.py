from django.urls import path
from .views import *

urlpatterns = [
    path('upload/', FileUploadView.as_view()),
    path('analyze/', AnalyzeView.as_view()),
    path('petitions/', RenderDocumentsView.as_view()),
    path('profile/', UserProfileView.as_view()),
]