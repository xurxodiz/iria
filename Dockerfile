FROM python:3.7-slim

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt
COPY . /code/
