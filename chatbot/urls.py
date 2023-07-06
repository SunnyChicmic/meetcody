from rest_framework import routers
from django.urls import path
from .views import summarizer,summarizer_with_prompt


urlpatterns = [
    path('', summarizer_with_prompt, name='summarizer'),
]
