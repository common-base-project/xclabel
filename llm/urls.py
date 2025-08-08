from django.urls import path

from .views import LlmView, provider as provider_views

app_name = 'llm'

urlpatterns = [
    path('chat', LlmView.api_chat),
    path('image', LlmView.api_image),
    path('video', LlmView.api_video),
    path('analyze', LlmView.api_analyze),
    path('providers', provider_views.list_providers),
    path('providers/create', provider_views.create_provider),
    path('providers/<int:pk>/update', provider_views.update_provider),
    path('providers/<int:pk>/delete', provider_views.delete_provider),
]
