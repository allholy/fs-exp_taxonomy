from django.db import models


# sounds for testing
class TestSound(models.Model):
    sound_id = models.CharField(max_length=50)
    sound_class = models.CharField(max_length=50)
    sound_group = models.IntegerField()
    sound_difficulty = models.CharField(max_length=3)

    def __str__(self):
        return f"<TestSound {self.sound_id}>"


# store input data for sounds
import csv
def csv_to_tuple_choices(csv_file):
    '''
    Import test choices (key and display name) from csv file.
    '''
    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        labels = next(reader)
        data = [(row[0], row[1]) for row in reader]
    tuple_choices = tuple(data)
    return(tuple_choices)

class SoundAnswer(models.Model):
    user_id = models.CharField(max_length=50)  # random generate
    test_sound = models.ForeignKey(TestSound, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Creation date', auto_now_add=True) #timezone aware

    # NOTE: If you change the keys, you have to be careful 
    # to change them manually in annotate_sound.html file.

    # available choices
    test_choices = csv_to_tuple_choices('classurvey/data/choices.csv')
    chosen_class = models.CharField(max_length=15, choices=test_choices, default="")
    likert_choices = ((1, 'Strongly Unconfident'), (2, 'Unconfident'), (3, 'Neutral'), (4, 'Confident'), (5, 'Strongly Confident'))
    confidence = models.IntegerField(choices=likert_choices,default="")


class ExitInfoModel(models.Model):
    answer = models.CharField(max_length=255, null=True, blank=True ,default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)

class UserDetailsModel(models.Model):
    ip_address = models.GenericIPAddressField(null=True)
    yes_no = (('Y', 'Yes'), ('N', 'No'))
    experience_choices = (('1', 'Nope'), ('2', 'Hobby'), ('3', 'Professional'))
    q1 = models.CharField(max_length=50,choices=yes_no,default="")
    q2 = models.IntegerField(null=True, blank=True)
    q3 = models.CharField(max_length=50,choices=experience_choices,default="")
    q4 = models.CharField(max_length=50,choices=yes_no,default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)