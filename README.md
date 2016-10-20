# django-boilerplate
How we start django projects

## Install Python environment

##### Install Python environment

`brew install python3`

`pip3 install virtualenvwrapper`

`source /usr/local/bin/virtualenvwrapper.sh`

`mkvirtualenv --python=/usr/local/bin/python3 django-boilerplate`

`workon django-boilerplate`

`pip install -r requirements/development.txt`

## Start developing
Despite the example code, you can make your own models.
When your are ready, generate migrations:
`python manage.py makemigrations hands_evaluator`

Then, apply it to database:
`python manage.py migrate`

The hands_evaluator is ready to admin the example models; check apps/hands_evaluator/admin.py.
Before you can browse the admin site, create a superuser:
`python manage.py createsuperuser`
with user "admx" and pass "admxpass".

After this, start the server:
`python manage.py runserver`

And play! Login to:
http://127.0.0.1:8000/admin/