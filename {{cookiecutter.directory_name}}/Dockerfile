FROM python:3.6

WORKDIR /usr/src/app
ENV PYTHONPATH /usr/src/app
ENV PYTHONUNBUFFERED 1

# Project Setup
RUN apt-get update -y && apt-get upgrade -y && apt-get install librabbitmq-dev libmemcached-dev libxml2-dev libxmlsec1-dev libxmlsec1-openssl -y

# Docker requirements
RUN pip install psycopg2-binary==2.8.3 sqlalchemy-utils alembic==1.0.11 alembic_autogenerate_enums==0.0.2 pymemcache==2.1.1 python-memcached==1.59

# Requirements
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY extras/scripts/entrypoint.sh extras/scripts/entrypoint.sh
RUN chmod 775 extras/scripts/entrypoint.sh && chmod u+s extras/scripts/entrypoint.sh

# Project files
USER 1000
COPY ./app ./app
COPY alembic.ini alembic.ini

# Run app
ENTRYPOINT ["extras/scripts/entrypoint.sh"]
