FROM python:3.10


SHELL ["/bin/bash", "-c"]

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

EXPOSE 8001

WORKDIR /sitemotorcycles
RUN mkdir /sitemotorcycles/static && mkdir /sitemotorcycles/media

COPY requirements.txt requirements.txt



RUN pip install -r requirements.txt

RUN pip install --upgrade pip

RUN apt update


COPY . .


CMD ["gunicorn", "-b", "0.0.0.0:8000", "sitemotorcycles.wsgi:application"]