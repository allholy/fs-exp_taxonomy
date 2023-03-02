from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import SoundAnswer, TestSound
from .forms import SoundAnswerForm


def home_view(request):
    return render(request, 'classurvey/home.html')


#test one question
def annotate_sound(request):

    import random
    test_sound = random.choice(TestSound.objects.all())

    form = SoundAnswerForm(request.POST or None)

    if request.POST:
        if form.is_valid():
            sound_answer = form.save(commit=False)
            sound_answer.test_sound_id = request.POST.get("test_sound_id")
            # TODO: save user id here 
            sound_answer.save()
            # redirect to next sound

            print(f"number of answers {SoundAnswer.objects.count()}")
            return HttpResponseRedirect(reverse('classurvey:main'))
        
    return render(request, 'classurvey/annotate_sound.html', {'test_sound': test_sound, 'form': form})