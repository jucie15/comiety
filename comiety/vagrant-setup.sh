#!/bin/sh

PG_VERSION='9.6'
POSTGIS_VERSION='2.3'

APP_DB_USER='comiety'  # FIXME: DB유저명. 수정해주세요.
APP_DB_NAME='comiety'  # FIXME: DB명. 수정해주세요.
APP_DB_PASS='ehdwlq123'  # FIXME: DB암호. 수정해주세요.

# postgresql 9.6
add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
apt-get update

apt-get install -y build-essential git python3 python3-pip python3-dev python3-gdal \
    libreadline-dev libssl-dev libbz2-dev libjpeg8-dev libpcre3 libpcre3-dev \
    libmagickwand-dev rdate libyaml-dev \
    rabbitmq-server \
    memcached libmemcached-dev redis-server \
    libgeos-dev libgdal1-dev libxslt1-dev libproj-dev \
    postgresql libpq-dev postgresql-client postgresql-client-common \
    postgresql-${PG_VERSION}-postgis-${POSTGIS_VERSION} \
    postgresql-${PG_VERSION}-postgis-scripts \
    postgresql-server-dev-${PG_VERSION} \
    nginx

cat << EOF | su - postgres -c psql
    DROP DATABASE IF EXISTS ${APP_DB_NAME};
    DROP USER IF EXISTS ${APP_DB_USER};

    CREATE USER ${APP_DB_USER} WITH PASSWORD '${APP_DB_PASS}';
    CREATE DATABASE ${APP_DB_NAME} WITH OWNER=${APP_DB_USER};

    \connect ${APP_DB_NAME};

    CREATE EXTENSION postgis;
    CREATE EXTENSION fuzzystrmatch;
    CREATE EXTENSION postgis_tiger_geocoder;
    CREATE EXTENSION postgis_topology;
EOF
