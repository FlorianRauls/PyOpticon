FROM python:3-alpine

RUN apk add gcc musl-dev linux-headers python3-dev
RUN pip install --no-binary :all: psutil

ADD \src\ .

ENTRYPOINT python entry.py

CMD ["python", "entry.py", "enp0s8"]