FROM python:3.7-alpine
WORKDIR /code
COPY . /code
CMD ["echo"] ["'Hello world'"]