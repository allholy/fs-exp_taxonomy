from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import SoundAnswer, TestSound
from .forms import SoundAnswerForm, UserDetailsForm, ExitInfoForm

import random


def user_id_from_request(request):
    user_id = request.session.get('user_id', None)
    if user_id is None:
        user_id = 'user_' + str(random.randint(10, 9999999))
        request.session['user_id'] = user_id
    return user_id

def get_ip_address(request):
    user_ip_address = request.META.get('HTTP_X_FORWARDED_FOR')
    if user_ip_address:
        return user_ip_address.split(',')[0]
    else:
        return request.META.get('REMOTE_ADDR')

def assign_group(request, user_id):
    ''' 
    Assign one group to the user and save it to the session.
    '''
    # see on the given table how many groups exist
    available_groups = TestSound.objects.values_list(
        'sound_group', flat=True).distinct()
    # groups done. if it is empty, none are done.
    groups_already_done = SoundAnswer.objects.filter(user_id=user_id).values_list(
        'test_sound__sound_group', flat=True).distinct()
    print(groups_already_done)

    if not len(groups_already_done) == len(available_groups):
        remaining_groups = set(available_groups) - set(groups_already_done)
        selected_group = random.choice(list(remaining_groups))
        print(selected_group)
        request.session['group_number'] = selected_group
        return selected_group
    else:
        # when none, redirect to a page that says they tested all sounds.
        return None

def get_next_sound_for_user(request):
    '''
    Retrieve the sounds that belong to a group and each time return one random
    sound until no more sound are remaining. 
    '''
    user_id = user_id_from_request(request)
    group_number = request.session['group_number']

    test_sound_ids_in_group = TestSound.objects.filter(
        sound_group=group_number).values_list('id', flat=True)
    test_sound_ids_already_answered = SoundAnswer.objects.filter(
        test_sound_id__in=test_sound_ids_in_group, user_id=user_id).values_list('test_sound_id', flat=True)

    remaining_sounds = TestSound.objects.filter(
        sound_group=group_number).exclude(id__in=test_sound_ids_already_answered)

    if not remaining_sounds:
        return None
    else:
        next_sound = random.choice(remaining_sounds)
        return next_sound


def sounds_sizes(request):
    '''
    Returns the total size of sounds and how many are answered already.
    '''
    user_id = user_id_from_request(request)
    group_number = request.session['group_number']

    test_sound_ids_in_group = TestSound.objects.filter(
        sound_group=group_number).values_list('id', flat=True)
    test_sound_ids_already_answered = SoundAnswer.objects.filter(
        test_sound_id__in=test_sound_ids_in_group, user_id=user_id).values_list('test_sound_id', flat=True)

    total_sounds_size = len(test_sound_ids_in_group)
    answered_sounds_size = len(test_sound_ids_already_answered)
    return total_sounds_size, answered_sounds_size


def home_view(request):
    user_id = user_id_from_request(request)
    group = assign_group(request, user_id)
    if None == group:
        return redirect(reverse('classurvey:group_end'))
    return render(request, 'classurvey/home.html')


def group_end_view(request):
    return render(request, 'classurvey/group_end.html')


def instructions_view(request):
    return render(request, 'classurvey/instructions.html')

import csv
def load_classes_from_csv(csv_file):
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        topclasses = {}
        for row in reader:
            topclass = row['TopClass']
            subclass = row['ClassName']
            if topclass not in topclasses:
                topclasses[topclass] = []
            topclasses[topclass].append(subclass)
    return topclasses

def taxonomy_view(request):
    classes = load_classes_from_csv('classurvey/data/choices.csv')
    print(classes)
    return render(request, 'classurvey/taxonomy.html', {'classes': classes})

def user_details_view(request):
    '''
    Form with user data and ip address.
    '''
    ip_address = get_ip_address(request)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ip_address = ip_address
            response.save()
            return redirect(reverse('classurvey:main'))
    else:
        form = UserDetailsForm()
    return render(request, 'classurvey/user_details.html', {'form': form})

# test one question
def annotate_sound_view(request):

    user_id = user_id_from_request(request)

    all_sounds_size, answered_sounds_size = sounds_sizes(request)

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
        # request.session['next_sound'] = test_sound
        if test_sound is None:
            return redirect(reverse('classurvey:exit_info'))

    return render(request, 'classurvey/annotate_sound.html', {
        'test_sound': test_sound, 'form': form,
        'all_sounds_size': all_sounds_size, 'answered_sounds_size': answered_sounds_size,
    })

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


@login_required
def results_view(request):
    return render(request, 'classurvey/results.html')