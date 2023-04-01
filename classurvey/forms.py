from django import forms
from .models import SoundAnswer, ExitInfoModel, UserDetailsModel


class SoundAnswerForm(forms.ModelForm):

    class Meta:
        model = SoundAnswer
        fields = ('chosen_class',)
        labels = {'chosen_class':'Which is the most suitable category for this sound?'}
        widgets = {
            'chosen_class': forms.RadioSelect,
        }


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = UserDetailsModel
        fields = '__all__'
        labels = {
            'q1':'Are you a Freesound user?',
            'q2':'If so, how many sounds have you uploaded (approximately)?',
            'q3':'Do you have experience with music technology?',
            'q4':'Are you a musician?',
        }
        widgets = {
            'q1': forms.RadioSelect,
            'q2': forms.NumberInput(attrs={'min':0,'max':49999}),
            'q3': forms.RadioSelect,
            'q4': forms.RadioSelect,
        }


class ExitInfoForm(forms.ModelForm):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 50}), 
        label='Do you have anything to say little user?',
        required=False
    )

    class Meta:
        model = ExitInfoModel
        fields = ('answer',)
