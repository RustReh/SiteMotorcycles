from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.forms import widgets

from .models import KindOfMotorcycle, EngineType, Motorcycles, Favorite


class AddPublicationForm(forms.ModelForm):
    kind = forms.ModelChoiceField(
        queryset=KindOfMotorcycle.objects.all(),
        empty_label='Класс не выбран',
        label='Класс',
    )

    type = forms.ModelChoiceField(
        queryset=EngineType.objects.all(),
        empty_label='Выберите тип двигателя',
        label='Тип двигателя',
    )

    class Meta:
        model = Motorcycles
        fields = ['photo', 'brand', 'bike_model', 'slug', 'description', 'kind', 'type']
        widgets = {
            'brand': forms.TextInput(),
            'bike_model': forms.TextInput(),
            'description': forms.Textarea(),
        }
        labels = {'slug': 'URL'}

    def clean_bike_model(self):
        bike_model = self.cleaned_data['bike_model']
        if len(bike_model) > 50:
            raise ValidationError("Длина превышает 50 символов")

        return bike_model


class AddToFavForm(forms.ModelForm):
    class Meta:
        model = Favorite
        fields = '__all__'