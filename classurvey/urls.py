from django.urls import path
from . import views

app_name = 'classurvey'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('instructions/', views.instructions_view, name='instructions'),
    path('details/', views.user_details_view, name='user_details'),
    path('question/',views.annotate_sound_view, name='main'),
    path('exit-info/', views.exit_info_view, name='exit_info'),
    path('end/', views.end_view, name='end'),
    path('group-end/', views.group_end_view, name='group_end'),
]