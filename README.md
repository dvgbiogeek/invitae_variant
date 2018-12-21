Project setup

(Using python3.5)

Create the environment

$ virtualenv variants
$ source variants/bin/activate
$ cd invitae_variant
$ pip install -r requirements.txt

Database setup
$ python manage.py makemigrations
$ python manage.py migrate

Data Import uses a django manager command

$ python manage.py runscript import_variants --script-args=variants/scripts/data/variants.tsv.zip

Start the server

$ python manage.py runserver

For the API endpoints Navigate to:

http://127.0.0.1:8000/api/{gene name} - Partial names to find list of genes

http://127.0.0.1:8000/api/variants/{gene name}

To run the tests:

$ python manage.py test
