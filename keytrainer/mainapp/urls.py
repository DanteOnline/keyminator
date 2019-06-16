from django.urls import path
from .views import MainTemplateView, OfficeTemplateView

app_name = 'mainapp'

urlpatterns = [
    path('', MainTemplateView.as_view(), name='main'),
    path('office/', OfficeTemplateView.as_view(), name='office'),
]
