# Semirhage reborn

The API backend for Tajm.me time tracking, powered by Django and Python 3.

## Setup

Requirements:

* Python 3 (3.5 will work fine)
* SQLite
* Virtualenv

```bash
virtualenv /path/to/venv
. /path/to/venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit the site at http://localhost:8000. This installs a SQLite database for local development.


## API Auth Quickstart


Create a client on http://localhost:8000/oauth2/applications with Resource owner password as grant type. Copy the generated
client id.

Generate access token using password grant, using the superuser recently created:

```
curl -d 'grant_type=password&client_id=<client_id>&username=<username>&password=<password>' http://localhost:8000/oauth2/token/
```

Use token in above response.

```
curl -H 'Authorization: bearer yxe3bTtUJnI6hc0ukVH5pQsdt5PKIP' -H 'Accept: application/vnd.api+json' http://localhost:8000/users/
```

For a pretty and readable output:

```
curl -H 'Authorization: bearer yxe3bTtUJnI6hc0ukVH5pQsdt5PKIP' -H 'Accept: application/vnd.api+json; indent=2' http://localhost:8000/users/
```

## Component overview

* Oauth 2, using [Django OAuth toolkit](https://django-oauth-toolkit.readthedocs.org)
* [Django REST Framework](http://www.django-rest-framework.org)
  * JSONAPI 1.0 spec, by [Django REST Framework JSON API](http://django-rest-framework-json-api.readthedocs.org)


## What about that bad-ass name?

This repo is named after one of the female Forsakens in Wheel of Time, the series of epic fantasy novels. This is said about [Semirhage](http://wot.wikia.com/wiki/Semirhage):

> Semirhage was among the most prominent Restorers, or healers, in the Age of Legends, and even before turning to the Shadow she was known to be cruel, often needlessly causing people extra pain when Healing them. Among the Forsaken she was the most depraved and sadistic, known for her unsurpassed skill with torturing and the pleasure she took in it, and she was in general the one people were most afraid to fall into the hands of for that reason.