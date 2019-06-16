from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
class MainTemplateView(TemplateView):
    template_name = 'mainapp/index.html'


class OfficeTemplateView(TemplateView):
    template_name = 'mainapp/office/office.html'