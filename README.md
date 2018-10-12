# Tajm time tracking

Yet another time tracking suite, built out of frustration regarding daily pain of using really bad
time trackers.

It is also a side project to discover Python 3, Django, DRF, OAuth 2 and progressive web apps.

This git repository contains the API backend, the evaluation UI frontend and the web-based admin.

## Setup

Requirements:

* Python 3 (3.5 will work fine)
* PostgreSQL
* Virtualenv

To use MySQL or other database alternatives, it is recommended to create a settings file
(using `tajm/settings.py` as a starting point) and use the
`--settings` flag when running `manage.py`. More info: [Django docs regarding manage.py](https://docs.djangoproject.com/en/1.10/ref/django-admin/#cmdoption-settings).

```bash
virtualenv -p $(which python3) /path/to/venv
. /path/to/venv/bin/activate
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver
```

Visit the site at http://localhost:8000, and the admin at http://localhost:8000/admin.


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

* [Django](https://docs.djangoproject.com/en/1.10/), the web framework for perfectionists with deadlines.
* OAuth 2, using [Django OAuth toolkit](https://django-oauth-toolkit.readthedocs.org)
* [Django REST Framework](http://www.django-rest-framework.org)
  * JSONAPI 1.0 spec, by [Django REST Framework JSON API](http://django-rest-framework-json-api.readthedocs.org)
* [Twitter Bootstrap](https://getbootstrap.com), version 3.3.7
* [Paper](http://bootswatch.com/paper/), a Twitter Bootstrap theme by [Bootswatch](http://bootswatch.com/lumen/).


## Contributions are welcome, so is feedback!

Fork or write an issue with your thoughts. Don't be a stranger.
