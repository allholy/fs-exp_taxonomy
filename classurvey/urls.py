from django.urls import path
from . import views

app_name = 'classurvey'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('question/',views.annotate_sound, name='main'),
]