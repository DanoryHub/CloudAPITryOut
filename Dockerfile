FROM python:3.8-alpine

WORKDIR /app

COPY . /app

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev 

RUN pip install -r requirements.txt 

EXPOSE 8000

CMD ["python", "app.py"]