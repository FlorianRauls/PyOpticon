FROM python:3.8-slim-buster

RUN pip install --upgrade pip

RUN pip install flask
RUN pip install mysql-connector-python
RUN pip install pandas
RUN pip install dash
RUN pip install mysql-connector-python

ADD . .

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["python", "app.py"]
