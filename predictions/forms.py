from django import forms
#from .models import Interaction
from django.contrib.auth.models import User

class InteractionForm(forms.ModelForm):
    class Meta:
        model = Interaction
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['student'].queryset = User.objects.filter(groups__name="Student")
