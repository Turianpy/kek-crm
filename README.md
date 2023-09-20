# kek-crm ![crm_workflow](https://github.com/Turianpy/kek-crm/actions/workflows/main.yaml/badge.svg)
just a simple crm

to start the server:

- Clone the repo
- Make sure 80 and 5432 are unoccupied or change ports in infra/.env yourself
- cd into infra
- create a .env file (you can specify your own values or copy from below)
'''
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=psql1337
DB_HOST=crm_db
DB_PORT=5432
SECRET_KEY='django-insecure-2d3=i3msfc^dkm8_rnxwo)r9%+ez)w7)iqtvn%zw6t_7_!jb!o'
DJANGO_DEBUG=True
'''

- docker-compose up


Docs should be available at localhost/api/docs/
