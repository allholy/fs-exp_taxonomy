from django.core.management.base import BaseCommand
from classurvey.models import TopLevel

import csv
import os


class Command(BaseCommand):
    help = 'Path for file with descriptions about the top level classes.'

    def add_arguments(self, parser):
        parser.add_argument('path', nargs='+', type=str)

    def handle(self, *args, **options):
        path = options['path'][0]
        if not os.path.exists(path):
            self.stderr.write(self.style.ERROR(f"The path '{path}' does not exist."))
            return
            
        self.stdout.write(self.style.SUCCESS(f"Importing data from '{path}'."))

        import_top_class_description_csv(path)


def import_top_class_description_csv(file_path):
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            sound,_ = TopLevel.objects.get_or_create(
                top_level_name=row['TopLevel'],
                top_level_description=row['Description'],
            )