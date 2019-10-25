FROM python:3.7-buster

COPY setup.py Pipfile Pipfile.lock /srv/

COPY deployment/entrypoint.sh /

WORKDIR /srv

COPY ./backend /srv/backend
COPY ./cleanslate /srv/cleanslate
COPY ./RecordLib /srv/RecordLib
COPY ./templates /srv/templates
COPY ./frontend/bundles /srv/frontend/bundles
COPY ./webpack-stats.json /srv
COPY ./manage.py /srv

RUN pip install pipenv && pipenv install --system && apt update && \
    apt install -y poppler-utils && \
    useradd -ms /bin/bash gunicorn && \
    #chmod o+x /entrypoint.sh && \
    mkdir -p /srv/static && \
    chown gunicorn:gunicorn /srv/static

USER gunicorn

ENV STATIC_ROOT /srv/static

EXPOSE 8000


#ENTRYPOINT ["/entrypoint.sh"]