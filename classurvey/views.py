from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from .models import SoundAnswer, TestSound, ClassChoice
from .forms import SoundAnswerForm, UserDetailsForm, ExitInfoForm

import random


def user_id_from_request(request):
    ''' Generate random user id. '''
    user_id = request.session.get('user_id', None)
    if user_id is None:
        user_id = 'user_' + str(random.randint(10, 9999999))
        request.session['user_id'] = user_id
    return user_id

def make_sound_order(request):
    group_number = request.session['group_number']

    # retrieve sound ids for one group
    test_sound_ids_in_group = TestSound.objects.filter(sound_group=group_number).values_list('id', flat=True)

    sound_order = request.session.get('sound_order', None)
    if sound_order is None:
        sound_order = list(test_sound_ids_in_group)
        random.shuffle(sound_order)

        request.session['sound_order'] = sound_order
        print(request.session['sound_order'])
    return sound_order

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

    # check if all groups are done. 
    if not len(groups_already_done) == len(available_groups):
        remaining_groups = set(available_groups) - set(groups_already_done)
        selected_group = random.choice(list(remaining_groups))
        request.session['group_number'] = selected_group
        request.session['sound_order'] = None
        print(selected_group)
        return selected_group
    else:
        # when none, redirect to a page that says they tested all sounds.
        return 'done'

def get_next_sound_for_user(request):
    '''
    Retrieve the sounds that belong to a group and each time return one random
    sound until no more sound are remaining. 
    '''
    user_id = user_id_from_request(request)
    group_number = request.session['group_number']
    ordered_sound_ids = make_sound_order(request)
    # unique answered sounds
    test_sound_ids_already_answered = SoundAnswer.objects.filter(
        test_sound_id__in=ordered_sound_ids, user_id=user_id, test_sound__sound_group=int(group_number)).values_list(
        'test_sound_id', flat=True).distinct()
    current_sound_index = len(ordered_sound_ids) - len(test_sound_ids_already_answered) 
    if 0 == current_sound_index:
        return None
    else:
        next_sound_id = ordered_sound_ids[current_sound_index-1]
        next_sound = TestSound.objects.get(id=next_sound_id)
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

def get_test_descriptions():
    ''' Get descriptions for each category. '''
    test_choices = ClassChoice.objects.values_list(
        'class_key', 'description', 'examples')
    return test_choices


def home_view(request):
    user_id = user_id_from_request(request)
    group = assign_group(request, user_id)
    if 'done' == group:
        return redirect(reverse('classurvey:group_end'))
    return render(request, 'classurvey/home.html')

def group_end_view(request):
    return render(request, 'classurvey/group_end.html')

def instructions_view(request):
    return render(request, 'classurvey/instructions.html')

def taxonomy_view(request):
    top_levels = ClassChoice.objects.values_list('top_level',flat=True).distinct()
    level_group = {}
    for top_level in top_levels:
        rows = ClassChoice.objects.filter(top_level=top_level)
        level_group[top_level] = list(rows)    
    return render(request, 'classurvey/taxonomy.html', {'level_group': level_group})

def user_details_view(request):
    '''
    Form with user data and ip address.
    '''
    ip_address = get_ip_address(request)

    if request.method == 'POST':
        form = UserDetailsForm(request.POST)
        if form.is_valid():
            request.session['user_details'] = form.cleaned_data
            request.session.save()

            response = form.save(commit=False)
            response.ip_address = ip_address
            response.user_id = request.session['user_id']
            response.save()
            return redirect(reverse('classurvey:main'))
    else:
        # store user details to prefill
        stored_user_details = request.session.get('user_details', None)
        form = UserDetailsForm(initial=stored_user_details)
    return render(request, 'classurvey/user_details.html', {'form': form})

# test one question
def annotate_sound_view(request):

    user_id = user_id_from_request(request)

    all_sounds_size, answered_sounds_size = sounds_sizes(request)
    current_sound_number = answered_sounds_size + 1

    if request.POST:
        form = SoundAnswerForm(request.POST)

        test_sound = TestSound.objects.get(id=request.POST.get('test_sound_id'))

        if form.is_valid():
            existing_sound_answer = SoundAnswer.objects.filter(test_sound=test_sound, user_id=user_id)
            if existing_sound_answer:
                existing_sound_answer = existing_sound_answer[0]
                existing_sound_answer.date_created = timezone.now()
                existing_sound_answer.chosen_class = form.cleaned_data['chosen_class']
                existing_sound_answer.confidence = form.cleaned_data['confidence']
                existing_sound_answer.save()
            else: 
                sound_answer = form.save(commit=False)
                sound_answer.test_sound_id = request.POST.get('test_sound_id') # sound id_not FS id
                sound_answer.user_id = user_id
                sound_answer.save()
            # print(f'number of answers {SoundAnswer.objects.count()}')
            return redirect(reverse('classurvey:main'))
    else:
        test_sound = get_next_sound_for_user(request)
        if test_sound is None:
            return redirect(reverse('classurvey:exit_info'))
        form = SoundAnswerForm()
        # request.session['next_sound'] = test_sound
   
    filename = test_sound.sound_name

    return render(request, 'classurvey/annotate_sound.html', {
        'test_sound': test_sound, 'form': form,
        'all_sounds_size': all_sounds_size, 'answered_sounds_size': current_sound_number, 'filename': filename,
        'class_titles': {class_key:f'{class_description} ({class_example})' for class_key, class_description, class_example in get_test_descriptions()}
    })

def exit_info_view(request):
    if request.method == 'POST':
        form = ExitInfoForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user_id = request.session['user_id']
            response.save()
            return redirect(reverse('classurvey:end'))
    else:
        form = ExitInfoForm()
    return render(request, 'classurvey/exit_info.html', {'form': form})

def end_view(request):
    return render(request, 'classurvey/end_page.html')

def informed_consent_view(request):
    return render(request, 'classurvey/informed_consent.html')

from collections import Counter
from django.db.models import Count
@login_required
def results_view(request):
    data = SoundAnswer.objects.values(
        'test_sound__sound_id', 'user_id', 
        'test_sound__sound_class', 'test_sound__sound_group', 'chosen_class', 
    )
    all_data_count = data.count()
    user_count = len(set(d['user_id'] for d in data.distinct())) #data.distinct('user_id').count()
    total_answers_data = data.values('test_sound__sound_group', 'user_id')
    total_answers = total_answers_data.annotate(count=Count('id', distinct=True)).count()
    group_counts = total_answers_data.distinct()
    group_counts = dict(Counter(d['test_sound__sound_group'] for d in group_counts))

    return render(request, 'classurvey/results.html',  {
        'all_data_count':all_data_count, 'user_count':user_count, 
        'total_answers':total_answers, 'group_counts':group_counts
    })