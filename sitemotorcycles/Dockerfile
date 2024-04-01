FROM python:3.10


SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN pip install --upgrade pip

RUN apt update && apt -qy install gcc libjpeg-dev libxslt-dev \
    libpq-dev libmariadb-dev libmariadb-dev-compat gettext cron openssh-client flake8 locales vim

RUN useradd -rms /bin/bash sm && chmod 777 /opt /run

WORKDIR /sm

RUN mkdir /sm/static && mkdir /sm/media && chown -R sm:sm /sm && chmod 755 /sm

COPY --chown=rustem:sm . .

RUN pip install -r requirements.txt

USER sm

CMD ["python manage.py -runserver","sitemotorcycles.wsgi:application"]