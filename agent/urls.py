from django.urls import path

from . import views

app_name = 'agent'

urlpatterns = [
    path('chat', views.chat),
    path('workflow/execute', views.execute_workflow),
]
