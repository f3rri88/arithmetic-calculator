FROM python:3.7-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY server.py /app/
COPY server /app/server
COPY client.py /app/
COPY client /app/client
COPY test.py /app/
COPY tests /app/tests
RUN mkdir /app/logs