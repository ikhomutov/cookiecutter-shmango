FROM python:3.7

WORKDIR /app
COPY requirements /app/requirements

ENV PYTHONPATH "${PYTHONPATH}:/app"
ENV PYTHONUNBUFFERED 1

RUN pip install -r requirements/prod.txt

COPY docker /app/docker
COPY {{ cookiecutter.project_slug }} /app/{{ cookiecutter.project_slug }}

RUN django-admin collectstatic --noinput --settings {{ cookiecutter.project_slug }}.settings.base

EXPOSE 8000

CMD ["gunicorn", "-c", "/app/docker/configs/gunicorn.conf", "{{ cookiecutter.project_slug }}.wsgi:application"]
