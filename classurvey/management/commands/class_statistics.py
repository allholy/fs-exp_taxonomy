from django.core.management.base import BaseCommand
from classurvey.models import TestSound, SoundAnswer

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt


class Command(BaseCommand):
    help = 'stats.'

    def handle(self, *args, **options):
        stats()


def stats():
    # by class

    data = SoundAnswer.objects.values(
        'test_sound__sound_id','test_sound__sound_class','chosen_class',
        'user_id'
    )
    count = data.count()
    print(count,data)

    #data.filter(='')

    ground_truth = [d['test_sound__sound_class'] for d in data]    
    user_answer = [d['chosen_class'] for d in data]

    user_count = set(d['user_id'] for d in data) # or query .distinct
    #print(ground_truth,user_answer)

    # confusion matrix
    cm = pd.crosstab(ground_truth, user_answer, normalize='index')
    # remove other from ground truth
    class_order = [choice[0] for choice in SoundAnswer.test_choices] # order as in choices
    only_in_gt = [x for x in class_order if not x.endswith("-other")]
    cm =cm.reindex(index=only_in_gt,columns=class_order,fill_value=0)

    fig, ax = plt.subplots(figsize=(15, 15))
    s = sb.heatmap(cm, annot=True, cmap='viridis', ax=ax)
    s.set_ylabel('Ground Truth', fontsize=15)
    s.set_xlabel('User Answer', fontsize=15)
    s.set_xticklabels(s.get_xticklabels(), rotation=45)
    s.set_yticklabels(s.get_yticklabels(), rotation=45)
    plt.show()
