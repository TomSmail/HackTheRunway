FROM python:3.10.5-bullseye 
# This is the version I used for dev

RUN mkdir ./uploads


RUN mkdir -p /app
WORKDIR /app

RUN mkdir ./uploads



COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python3", "wsgi.py"]
