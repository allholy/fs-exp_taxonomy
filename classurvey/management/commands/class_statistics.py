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

    data = SoundAnswer.objects.values('test_sound__sound_id','test_sound__sound_class','chosen_class')
    ground_truth = [d['test_sound__sound_class'] for d in data]    
    user_answer = [d['chosen_class'] for d in data]

    # confusion matrix
    cm = pd.crosstab(ground_truth, user_answer, normalize='index')
    class_order = [choice[0] for choice in SoundAnswer.test_choices]
    cm =cm.reindex(index=class_order,columns=class_order,fill_value=0)

    s = sb.heatmap(cm, annot=True, cmap='viridis')

    s.set_ylabel('Ground Truth', fontsize=16)
    s.set_xlabel('User Answer', fontsize=16)
    plt.show()
