FROM python:3.8.2-alpine3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

EXPOSE 8000

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt && rm requirements.txt

COPY . /code/
