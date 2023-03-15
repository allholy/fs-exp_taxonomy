from django.core.management.base import BaseCommand, CommandError
from classurvey.models import TestSound

import csv
import os

# path of data file as an argument
# your databse in a csv
class Command(BaseCommand):
    help = 'Path for file with data about the test sounds.'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['path'][0]
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"The path '{path}' does not exist."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Importing data from '{path}'."))

        import_sounds_csv(path)


# import data
def import_sounds_csv(file_path):
    #NOTE: remember to delete all existing data before re-upload
    #TestSound.objects.all().delete
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sound = TestSound.objects.create(
                sound_id=row['ID'],
                sound_class=row['Class'],
                sound_group=row['Group']
            )
