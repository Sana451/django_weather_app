from django import forms


class CityForm(forms.Form):
    city = forms.CharField(label="Название города", max_length=30,
                           widget=forms.TextInput(attrs={'placeholder': 'например: Москва'}))
