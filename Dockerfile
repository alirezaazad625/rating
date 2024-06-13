FROM python:3.12-alpine

WORKDIR /code

COPY src/requirements.txt /code/
RUN pip install -r requirements.txt

COPY src /code/