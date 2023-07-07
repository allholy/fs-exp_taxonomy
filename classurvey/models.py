from django.db import models

from multiselectfield import MultiSelectField


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
    examples = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"<ClassChoice {self.class_name}>"

class TopLevel(models.Model):
    top_level_name = models.CharField(max_length=10)
    top_level_description = models.CharField(max_length=255)

    def __str__(self):
        return f"<TopLevel {self.class_name}>"
    

class SoundAnswer(models.Model):
    user_id = models.CharField(max_length=50)  # random generate
    test_sound = models.ForeignKey(TestSound, on_delete=models.CASCADE)
    date_created = models.DateTimeField('Creation date', auto_now_add=True) #timezone aware

    # NOTE: If you change the keys, you have to be careful
    # to change them manually in annotate_sound.html file.

    # Import choices and put them in a tuple.
    chosen_class = models.CharField(max_length=15, default="")
    likert_choices = ((1, 'Very Unconfident'), (2, 'Unconfident'), (3, 'Neutral'), (4, 'Confident'), (5, 'Very Confident'))
    confidence = models.IntegerField(choices=likert_choices,default="")


class UserDetailsModel(models.Model):
    user_id = models.CharField(max_length=50) #, unique=True
    ip_address = models.GenericIPAddressField(null=True)

    yes_no = (('Y', 'Yes'), ('N', 'No'))
    experience_choices = (('1', 'No experience'), ('2', 'Experience as a hobbyist'), ('3', 'Experience as a professional'))
    areas_choices = (
        ('mr', 'Music or radio production'),
        ('f', 'Film making, game development, video creation'),
        ('s', 'Sound design'),
        ('mc', 'Music composition'),
        ('ex', 'Exploratory sound art, audio installations'),
        ('ed', 'Education'),
        ('r', 'Research')
    )

    q1 = models.CharField(max_length=50, choices=yes_no, default="")
    q2 = models.IntegerField(null=True, blank=True)
    q3 = models.CharField(max_length=50, choices=experience_choices, default="")
    q4 = models.CharField(max_length=50, choices=experience_choices, default="")
    q5 = MultiSelectField(choices=areas_choices, max_choices=25, max_length=255, blank=True, default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)


class ExitInfoModel(models.Model):
    # user_id = models.ForeignKey(UserDetailsModel, on_delete=models.CASCADE, to_field='user_id')
    user_id = models.CharField(max_length=50)

    answer = models.CharField(max_length=750, null=True, blank=True, default="")
    date_created = models.DateTimeField('Creation date', auto_now_add=True)