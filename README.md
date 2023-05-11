# Platform for taxonomy experiment. 

This repository contains the source code of the taxonomy experiment in Freesound.

## How to setup

1. Clone the repo and make the Django migrations for creating the models.
2. To import the necessary data, you would have to request the files that have the available classes and the sounds data (`class_choices.csv` and `sounds_for_experiment.csv`).
You can import them by running `python manage.py import_classes` and `python manage.py import_sounds` respectively.
