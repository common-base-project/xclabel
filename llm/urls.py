from django.urls import path
from .views import provider

app_name = "llm"

urlpatterns = [
    path("providers/", provider.list_providers, name="provider-list"),
    path("providers/create/", provider.create_provider, name="provider-create"),
    path("providers/<int:pk>/update/", provider.update_provider, name="provider-update"),
    path("providers/<int:pk>/delete/", provider.delete_provider, name="provider-delete"),
]
