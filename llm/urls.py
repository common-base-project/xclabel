from django.urls import path
from .views import LlmView

app_name = 'llm'

urlpatterns = [
    path('chat', LlmView.api_chat),
    path('image', LlmView.api_image),
    path('video', LlmView.api_video),
    path('analyze', LlmView.api_analyze),
]
