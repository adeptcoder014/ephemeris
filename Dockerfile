FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y python3-dev python3-pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]
