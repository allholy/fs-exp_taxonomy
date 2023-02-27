from django.db import models


class TestSound(models.Model):
    sound_id = models.CharField(max_length=50)
    sound_class = models.CharField(max_length=50)

    def __str__(self):
        return self.sound_id
    