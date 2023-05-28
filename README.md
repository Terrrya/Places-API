# Places API
<hr>

API service for managing places. You can search nearest place by coordinates. If it will two or more places you get 
them all.

## Features:
<hr>

- Admin panel: /admin/
- Documentation is located at: /api/doc/swagger/
- Managing places
- Search nearest places by coordinates

## Installing using GitHub
<hr>

## Run with Python

Python3 should be installed

```python
git clone https://github.com/Terrrya/Library-service.git
cd Library-service
python3 -m venv venv
source venv/bin/activate
```
Create in root directory of project and fill .env file as shown in .env_sample file

```python
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Open in browser 127.0.0.1:8000/api/

## Run with docker
<hr>

Docker should be installed

```python
git clone https://github.com/Terrrya/Library-service.git
cd Library-service
```

Create in root directory of project and fill .env file as shown in .env_sample file

```python
docker compose up
```
Open in browser 127.0.0.1:8000/api/ 

## Filling .env file
<hr>

To fill .env file you have to get API token of telegram bot and Stripe Secret API Token. 
<br> https://core.telegram.org/bots/faq#how-do-i-create-a-bot can help you to get Telegram API token
<br> https://stripe.com/docs/keys - can help you to get Stripe secret access key


## Getting access
<hr>

You can use following:
- superuser:
  - Username: admin
  - Password: 12345

Or create another one by yourself:
- create user via Admin panel /admin/

## Places API allows:

- via api/admin/ --- Work with admin panel
- via /api/doc/swagger/ --- Detail api documentation by swagger
- via [POST] /api/places/ --- Add new place
- via [GET] /api/places/ --- Places list
- via [GET] /api/places/pk/ --- Place detail information
- via [PUT, PATCH] /api/places/pk/ --- Update place information
- via [DELETE] /api/places/pk/ --- Delete place
