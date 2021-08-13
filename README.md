# comment_tree

## Description

Comment tree is a simple REST API app to implement a blogging function: users can post an article, and other users can comment the articles or leave a comment on other people's comment. API response for a comment contains ID of a parent comment (```Null``` if its zero-level comment) and nesting level (depth of the comment, 0 if the comment is left directly in response to an article). These fields allow one to recreate the comment tree structure, which is organized as a linked list.
Powered by nginx, Django, PostgreSQL.

## Settings

Default query for an article's comments includes only comments up to 3rd nesting level. Deeper comments can be called additionally by corresponding endpoint.

## Endpoints

Endpoints are created by REST DefaultRouter. API is versioned, api root is ```api/v1/```. Please note: CORS headers need to be configured additionally!

```hhtp://127.0.0.1/api/v1/articles``` returns paginated list of articles.
```hhtp://127.0.0.1/api/v1/articles/<article-id>``` returns specific article by id.
```hhtp://127.0.0.1/api/v1/articles/<article-id>/comments``` returns paginated article's comments UP TO third nesting level.
```hhtp://127.0.0.1/api/v1/articles/<article-id>/comments/<article-id>``` returns specific comment by id.
```hhtp://127.0.0.1/api/v1/articles/<article-id>/comments/<article-id>/child-comments``` returns comments of depth 4 and deeper for a specefic comment.

## Permissions

Default permission is rest_framework.permissions.IsAdminUser. Articles and Comments viewsets are rest_framework.permissions.IsAuthenticatedOrReadOnly.

## Setup

Clone project to your machine. Create .env file with database access specifications (DB_NAME, POSTGRES_USER, POSTGRES_PASSWORD, DB_HOST, DB_PORT) and SECRET_KEY (can be generated here: https://djecrety.ir)
From root direcrory of the project run:

```
docker-compose up -d --build
```

I prefer running migrations manually, to do that run following:

```
docker-compose exec web python manage.py makemigrations articles comments
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

To create superuser run:

```
docker-compose exec web python manage.py createseperuser
```

Apply initial data:

```
docker-compose exec web python manage.py loaddata fixtures.json
```

All is set! Now you can check the results at http://127.0.0.1/api/v1

## API Specs

After the setup API specifications can be found at http://127.0.0.1/swagger or http://127.0.0.1/redoc