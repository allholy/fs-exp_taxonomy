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


class UserDetailsForm(forms.Form):
    fsuser_choices = [('Y', 'Yes'), ('N', 'No')]
    experience_choices = [('1', 'Hobby'), ('2', 'Professional')]
    question1 = forms.ChoiceField(choices=fsuser_choices)
    question2 = forms.ChoiceField(choices=experience_choices)
