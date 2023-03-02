from django.db import models


# sounds for testing
class TestSound(models.Model):
    sound_id = models.CharField(max_length=50)
    sound_class = models.CharField(max_length=50)

    def __str__(self):
        return f"<TestSound {self.sound_id}>"
    

# store data 
class SoundAnswer(models.Model):
    # should be foreign key
    user_id = models.CharField(max_length=50)  # this can be FS ID or IP ADDRESS
    test_sound = models.ForeignKey(TestSound, on_delete=models.CASCADE)
    # available choices, test for now with few
    test_choices =(
        ("M-SOLO", "Solo"),
        ("M-MULT", "Multi"),
        ("FX-HOUSE", "House"),
        ("SP-CR", "Crowd")
    )
    chosen_class = models.CharField(max_length=15, choices=test_choices, default="")