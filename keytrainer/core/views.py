from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.list import MultipleObjectMixin

from .models import AbstractActivated


class ActivatedMultipleObjectsMixin(MultipleObjectMixin):

    def get_queryset(self):
        # TODO: что делать если поле называется по другому?
        return super().get_queryset().filter(is_active=True)

class UserMultipleObjectsMixin(MultipleObjectMixin):

    def get_queryset(self):
        # TODO: что делать если поле называется по другому?
        return super().get_queryset().filter(user=self.request.user)

# Create your views here.
class ActivatedListView(ListView):
    model = AbstractActivated

    def get_queryset(self):
        return self.model.activated.all()
