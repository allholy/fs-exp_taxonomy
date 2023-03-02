from django import forms
from .models import SoundAnswer


class SoundAnswerForm(forms.ModelForm):

    class Meta:
        model = SoundAnswer
        fields = ('chosen_class',)
        labels = {'chosen_class':'Which is the most suitable category for this sound?'}
        widgets = {
            'chosen_class': forms.RadioSelect,
        }
