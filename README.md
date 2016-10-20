# Pokertest

## HOW TO TEST

You have two options:

## Using public docker image (prefered)

##### Install docker, as described here:
https://www.docker.com/products/docker

##### ... then:
docker run -d -p 8000:8000 --name pokertest carloscaceres/pokertest

##### and play!:
localhost:8000/hands_evaluator/deals/start

## Install Python environment

##### Install Python environment

`brew install python3`

`pip3 install virtualenvwrapper`

`source /usr/local/bin/virtualenvwrapper.sh`

`mkvirtualenv --python=/usr/local/bin/python3 pokertest`

`workon pokertest`

`pip install -r requirements.txt`

##### ... then, start the server:

`python manage.py runserver`


##### and play!:

localhost:8000/hands_evaluator/deals/start


## Things to-do:
- Add tests
- Clean code
- Refactor models and add convenience methods
- Protect model's properties
