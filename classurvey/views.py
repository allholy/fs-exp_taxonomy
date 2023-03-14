from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import SoundAnswer, TestSound
from .forms import SoundAnswerForm
import random



def user_id_from_request(request):
    user_id = request.session.get("user_id", None)
    if user_id is None:
        user_id= "user_"+ str(random.randint(99,9999999))
        request.session["user_id"]= user_id
    return user_id


def home_view(request):
    user_id_from_request(request)
    return render(request, 'classurvey/home.html')


def get_next_sound_for_user(user_id):
    #if there are no more sounds, return none
    return random.choice(TestSound.objects.all())


#test one question
def annotate_sound(request):
    user_id = user_id_from_request(request)

    if request.POST:
        form = SoundAnswerForm(request.POST)
        test_sound = TestSound.objects.get(id=request.POST.get("test_sound_id"))
        if form.is_valid():
            sound_answer = form.save(commit=False)
            sound_answer.test_sound_id = request.POST.get("test_sound_id")
            sound_answer.user_id = user_id
            sound_answer.save()
            # redirect to next sound

            print(f"number of answers {SoundAnswer.objects.count()}")
            return HttpResponseRedirect(reverse('classurvey:main'))

    else:
        form = SoundAnswerForm()
        test_sound=get_next_sound_for_user(user_id)
        if test_sound is None:
            return HttpResponseRedirect(reverse('classurvey:exit'))

    return render(request, 'classurvey/annotate_sound.html', {'test_sound': test_sound, 'form': form})

