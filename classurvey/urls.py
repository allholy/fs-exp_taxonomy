from django.urls import path
from . import views

app_name = 'classurvey'

urlpatterns = [
    path('', views.closed_view, name='home'),
    path('instructions/', views.instructions_view, name='instructions'),
    path('taxonomy/', views.taxonomy_view, name='taxonomy'),
    path('details/', views.user_details_view, name='user_details'),
    path('question/',views.annotate_sound_view, name='main'),
    path('exit-info/', views.exit_info_view, name='exit_info'),
    path('end/', views.end_view, name='end'),
    path('group-end/', views.group_end_view, name='group_end'),
    path('results/', views.results_view, name='results'),
    path('informed-consent/', views.informed_consent_view, name='informed_consent'),
    path('export/', views.export_view, name='export'),
]