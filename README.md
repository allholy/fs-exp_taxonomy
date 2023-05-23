# Platform for taxonomy experiment. 

This repository contains the source code of the taxonomy experiment in Freesound.

## How to setup

1. Clone the repo and make the Django migrations for creating the models.
2. To import the necessary data, you would have to request the files that have the available classes and the sounds data (`class_choices.csv` and `sounds_for_experiment.csv`).
You can import them by running `python manage.py import_classes` and `python manage.py import_sounds` respectively.



## Instructions for Docker

1. Copy `class_choices.csv` and `sounds_for_experiment.csv` to `classurvey/data/` folder.

2. `docker-compose build`

3. `docker-compose run --rm app python manage.py migrate`

4. `docker-compose run --rm app python manage.py import_classes /code/classurvey/data/class_choices.csv`

5. `docker-compose run --rm app python manage.py import_sounds /code/classurvey/data/sounds_for_experiment.csv`

6. `docker-compose run --rm app python manage.py createsuperuser`

7. `docker-compose up`

8. Open `localhost:8500/` to see the experiment page.

If you want to run an interactive python shell:

`docker-compose run --rm app python manage.py shell_plus`
