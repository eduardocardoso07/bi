from django import forms
from sistem.models import Brindes, Lancamentos

class BrindeForm(forms.ModelForm):
    class Meta:
        model = Brindes
        fields = '__all__'

class LancamentoForm(forms.ModelForm):
    class Meta:
        model = Lancamentos
        fields = '__all__'
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }