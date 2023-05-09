from django.db import models


# sounds for testing
class TestSound(models.Model):
    sound_id = models.CharField(max_length=50)
    sound_class = models.CharField(max_length=50)
    sound_group = models.IntegerField()
    sound_difficulty = models.CharField(max_length=3)
    sound_name = models.CharField(max_length=150)
    
    def __str__(self):
        return f"<TestSound {self.sound_id}>"


class ClassChoice(models.Model):
    class_key = models.CharField(max_length=10)
    class_name = models.CharField(max_length=50)
    top_level = models.CharField(max_length=20)
    description = models.CharField(max_length=255, null=True)
    examples = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f"<ClassChoice {self.class_name}>"

def get_test_descriptions():
    test_choices = ClassChoice.objects.values_list(
        'class_key', 'description', 'examples')
    return test_choices

def get_test_choices():
    ''' Import choices and put them in a tuple.'''
    test_choices = ClassChoice.objects.values_list(
        'class_key', 'class_name')
    test_choices = tuple(test_choices)
    return test_choices

class SoundAnswer(models.Model):
    user_id = models.CharField(max_length=50)  # random generate
    test_sound = models.ForeignKey(TestSound, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Creation date', auto_now_add=True) #timezone aware

    # NOTE: If you change the keys, you have to be careful
    # to change them manually in annotate_sound.html file.
    test_choices = get_test_choices() # available choices

    chosen_class = models.CharField(max_length=15, choices=test_choices, default="")
    likert_choices = ((1, 'Strongly Unconfident'), (2, 'Unconfident'), (3, 'Neutral'), (4, 'Confident'), (5, 'Strongly Confident'))
    confidence = models.IntegerField(choices=likert_choices,default="")


class UserDetailsModel(models.Model):
    user_id = models.CharField(max_length=50) #, unique=True
    ip_address = models.GenericIPAddressField(null=True)

    yes_no = (('Y', 'Yes'), ('N', 'No'))
    experience_choices = (('1', 'No'), ('2', 'Hobby'), ('3', 'Professional'))
    q1 = models.CharField(max_length=50,choices=yes_no,default="")
    q2 = models.IntegerField(null=True, blank=True)
    q3 = models.CharField(max_length=50,choices=experience_choices,default="")
    q4 = models.CharField(max_length=50,choices=experience_choices,default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)


class ExitInfoModel(models.Model):
    # user_id = models.ForeignKey(UserDetailsModel, on_delete=models.CASCADE, to_field='user_id')
    user_id = models.CharField(max_length=50)

    answer = models.CharField(max_length=750, null=True, blank=True ,default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)