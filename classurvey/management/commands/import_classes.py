from django.core.management.base import BaseCommand
from classurvey.models import ClassChoice

import csv
import os


class Command(BaseCommand):
    # The data is in csv file. Its path is an argument.
    help = 'Path for file with data about the classes (taxonomy).'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['path'][0]
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"The path '{path}' does not exist."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Importing data from '{path}'."))

        import_classes_csv(path)


def import_classes_csv(file_path):
    '''
    Import the classes data from csv file.
    '''
    #NOTE: remember to delete all existing data before re-upload
    #ClassChoice.objects.all().delete()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sound,_ = ClassChoice.objects.get_or_create(
                class_key=row['ClassKey'],
                class_name=row['ClassName'],
                top_level=row['TopLevel'],
                description=row['Description'],
                examples=row['Examples'],
            )