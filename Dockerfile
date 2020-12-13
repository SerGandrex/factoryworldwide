FROM python:3.7-alpine

RUN apk update
COPY factoryworldwide_app /app/factoryworldwide_app
COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt \
    &&  echo "$(pwd)" | tee /usr/local/lib/python3.7/site-packages/factoryworldwide_app.pth > /dev/null

WORKDIR /app/factoryworldwide_app/server
RUN pwd
RUN ls

ENV FLASK_APP=migrate.py
RUN flask db init
RUN flask db migrate
RUN flask db upgrade

EXPOSE 5000
CMD python RunServer.py