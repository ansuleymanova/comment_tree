FROM python:3.8.5
WORKDIR /code
COPY . .
RUN pip install -U pip && pip install -r requirements.txt
CMD gunicorn comment_tree.wsgi:application --bind 0.0.0.0:8000