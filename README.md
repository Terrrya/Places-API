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

## Run with docker
<hr>

Docker should be installed

```python
git clone https://github.com/Terrrya/test-gis
cd test-gis
```

Create in root directory of project and fill .env file as shown in .env_sample file

```python
docker compose up
```
Open in browser 127.0.0.1:8000/api/ 

## Filling .env file
<hr>

To fill .env file you have to use .env_smple as example.
To get Django secret key u can use https://djecrety.ir/ 
Also you can add settings for your database or use default settings from .env_smple


## Getting admin access
<hr>

You can use following:
- superuser:
  - Username: admin
  - Password: admin12345

Or create another one by yourself:
- create user via Admin panel /admin/

## Places API allows:

- via /api/admin/ --- Work with admin panel
- via /api/doc/swagger/ --- Detail api documentation by swagger
- via [POST] /api/places/ --- Add new place
- via [GET] /api/places/ --- Places list
- via [GET] /api/places/?coordinates=12.34,23.56 --- Places list nearest to coordinates = 12.34,23.56
- via [GET] /api/places/pk/ --- Place detail information
- via [PUT, PATCH] /api/places/pk/ --- Update place information
- via [DELETE] /api/places/pk/ --- Delete place
