# Map Project

## Changes

__27 April 2025__ <br>
Currently the application is functional but I need to check the code, correct it, translate it into English and check if there are any remaining bugs.

## About

It's a relatively easy-to-access tool for businesses to create interactive maps. It includes a global map and floor plans.
There's an administrator section with several roles and associated restrictions.

## Installation

I use Python 3.10 and Django

 > pip install poetry
 
Install all packages

> poetry install

## Prequesite

Externals assets :

 - bootstrap 5.3.3
 - fontawesome free 6.4.0
 - leaflet 1.9.4
 
 
```
floorproject/
├── administrator/
│   ├── templates/
│   │   ├── administrator/
│   │   │   ├── base.html
│   │   │   ├── cartes.html
│   │   │   ├── delete_user.html
│   │   │   ├── edit_carte.html
│   │   │   ├── edit_plans.html
│   │   │   ├── index.html
│   │   │   ├── login.html
│   │   │   ├── plans.html
│   │   │   ├── upload.html
│   │   │   ├── user_form.html
│   │   │   ├── users.html
│   ├── templatetags
│   │   ├── form_tags.py
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── decorators.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
├── floorproject/
│   ├── static/
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   ├── images/
│   │   │   │   ├── layers-2x.png
│   │   │   │   ├── layers.png
│   │   │   │   ├── marker-icon-2x.png
│   │   │   │   ├── marker-icon.png
│   │   │   │   ├── marker-shadow.png
│   │   │   ├── leaflet.css
│   │   ├── fontawesome/
│   │   │   ├── css/
│   │   │   ├── webfonts/
│   │   ├── img/
│   │   ├── js/
│   │   │   ├── bootstrap.bundle.min.js
│   │   │   ├── leaflet.js
│   │   ├── json/
│   │   │   ├── global_map.json
│   │   │   ├── maps.json
│   │   ├── plans/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
├── public/
│   ├── templates/
│   │   ├── public/
│   │   │   ├── base.html
│   │   │   ├── cartes.html
│   │   │   ├── index.html
│   │   │   ├── plans.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
├── manage.py
├── db.sqlite3
```

## How to run

Go to your `floorproject` folder and type

> python manage.py runserver

Credientials are `admin` and `admin`
