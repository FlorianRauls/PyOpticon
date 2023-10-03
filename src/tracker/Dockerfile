FROM python:3-alpine

RUN apk add gcc musl-dev linux-headers python3-dev
RUN pip install --no-binary :all: psutil
RUN pip install flask
RUN pip install mysql-connector-python
RUN pip install pyyaml

ADD . .

ENTRYPOINT python app.py