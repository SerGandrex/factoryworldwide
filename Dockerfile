FROM python:3.7-alpine

RUN apk update
COPY factoryworldwide_app /app/factoryworldwide_app
COPY requirements.txt /app
WORKDIR /app

RUN pip install -r requirements.txt \
    &&  echo "$(pwd)" | tee /usr/local/lib/python3.7/site-packages/factoryworldwide_app.pth > /dev/null

EXPOSE 5000
CMD python factoryworldwide_app/server/RunServer.py