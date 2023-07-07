from django import forms
from .models import SoundAnswer, ExitInfoModel, UserDetailsModel, ClassChoice


class SoundAnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        test_choices = ClassChoice.objects.values_list('class_key', 'class_name')
        self.fields['chosen_class'].widget = forms.RadioSelect(choices=tuple(test_choices))

    class Meta:
        model = SoundAnswer
        fields = ('chosen_class', 'confidence')
        labels = {
            'chosen_class': 'Which is the most suitable category for this sound?',
            'confidence': 'How confident are you about your answer?'
        }
        widgets = {
            'confidence': forms.RadioSelect,
        }


class UserDetailsForm(forms.ModelForm):

    class Meta:
        model = UserDetailsModel
        exclude = ['user_id','ip_address']
        labels = {
            'q1':'Are you a Freesound user?',
            'q2':'If so, how many sounds have you uploaded (approximately)?',
            'q3':'Do you have experience with audio/music technology?',
            'q4':'Do you have experience as a musician?',
            'q5':'Which of these areas have you practiced (if any)?',
        }
        widgets = {
            'q1': forms.RadioSelect,
            'q2': forms.NumberInput(attrs={'min':0,'max':49999}),
            'q3': forms.RadioSelect,
            'q4': forms.RadioSelect,
            'q5': forms.CheckboxSelectMultiple,
        }


class ExitInfoForm(forms.ModelForm):
    answer = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'textarea'}), 
        label='Thanks for annotating all sounds! Please use the space below to optionally provide any additional feedback that you might want to share about the taxonomy.',
        required=False
    )

    class Meta:
        model = ExitInfoModel
        exclude = ['user_id']
