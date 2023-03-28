from django.shortcuts import render,redirect

from django.urls import reverse
from .models import SoundAnswer, TestSound
from .forms import SoundAnswerForm, UserDetailsForm, ExitInfoForm
import random



def user_id_from_request(request):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        user_id = 'user_'+ str(random.randint(10,9999999))
        request.session['user_id'] = user_id
    return user_id

def assign_group(request,user_id):
    ''' 
    Assign one group to the user and save it to the session.
    '''
    available_groups = TestSound.objects.values_list('sound_group', flat=True).distinct()
    groups_already_done = SoundAnswer.objects.filter(user_id=user_id).values_list('test_sound__sound_group', flat=True).distinct()
    print(available_groups, groups_already_done)

    selected_group = request.session.get('group_number', None)
    if selected_group is None:
        # TODO: what happenes when they do all? -> remaining_groups
        # i want it to redirect to a page when they press button that says they tested all available sounds.
        remaining_groups = set(available_groups) - set(groups_already_done)
        selected_group = random.choice(list(remaining_groups))
        request.session['group_number'] = selected_group   
    return selected_group


def home_view(request):
    user_id = user_id_from_request(request)
    assign_group(request,user_id)
    return render(request, 'classurvey/home.html')


def get_next_sound_for_user(request):
    '''
    Retrieve the sounds that belong to a group and each time return one random
    sound until no more sound are remaining. 
    '''
    user_id = user_id_from_request(request)
    group_number = assign_group(request,user_id)

    test_sound_ids_in_group = TestSound.objects.filter(sound_group=group_number).values_list('id', flat=True)
    test_sound_ids_already_answered = SoundAnswer.objects.filter(test_sound_id__in=test_sound_ids_in_group, user_id=user_id).values_list('test_sound_id', flat=True)

    remaining_sounds = TestSound.objects.filter(sound_group=group_number).exclude(id__in=test_sound_ids_already_answered)

    if not remaining_sounds:
        return None
    else:
        next_sound = random.choice(remaining_sounds)
        return next_sound


#test one question
def annotate_sound(request):

    user_id = user_id_from_request(request)

    if request.POST:
        form = SoundAnswerForm(request.POST)
        test_sound = TestSound.objects.get(id=request.POST.get('test_sound_id'))

        if form.is_valid():
            sound_answer = form.save(commit=False)
            sound_answer.test_sound_id = request.POST.get('test_sound_id')
            sound_answer.user_id = user_id
            sound_answer.save()
            # redirect to next sound

            print(f'number of answers {SoundAnswer.objects.count()}')
            return redirect(reverse('classurvey:main'))

    else:
        form = SoundAnswerForm()
        test_sound = get_next_sound_for_user(request)
        if test_sound is None:
            return redirect(reverse('classurvey:exit_info'))

    return render(request, 'classurvey/annotate_sound.html', {'test_sound': test_sound, 'form': form})


def instructions_view(request):
    return render(request, 'classurvey/instructions.html')

def user_details_view(request):
    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            response = form.save()
            return redirect(reverse('classurvey:main'))
    else:
        form = UserDetailsForm()
    return render(request, 'classurvey/user_details.html', {'form': form})

def exit_info_view(request):
    if request.method == 'POST':
        form = ExitInfoForm(request.POST)
        if form.is_valid():
            response = form.save()
            return redirect(reverse('classurvey:end'))
    else:
        form = ExitInfoForm()
    return render(request, 'classurvey/exit_info.html', {'form': form})

def end_view(request):
    return render(request, 'classurvey/end_page.html')
