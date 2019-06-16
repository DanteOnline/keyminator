from bootstrap_app.forms import set_form_control
from django import forms
from .models import OrderLetters, Word


class OrderLettersEditForm(forms.ModelForm):
    # TODO: в последовательности не могут пофторятся буквы лучше реализовать в модели

    class Meta:
        model = OrderLetters
        fields = ('name','description')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_control(self.fields)


class WordEditForm(forms.ModelForm):
    # TODO: в последовательности не могут пофторятся буквы лучше реализовать в модели

    class Meta:
        model = Word
        exclude = ('unique_letters', 'slug')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        set_form_control(self.fields)


class UploadFileForm(forms.Form):
    file = forms.FileField()


