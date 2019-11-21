from django.urls import path
from .views import *

urlpatterns = [
    path("search/name/", SearchName.as_view()),
    path("download/", DownloadDocs.as_view()),
]