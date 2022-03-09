FROM python:3.8

WORKDIR /app

RUN apt-get update -y

RUN apt-get install python3-dev -y

COPY ./requirements.txt requirements.txt

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# CMD ["sh", "run.sh"]

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /
RUN ["chmod", "+x", "/wait-for-it.sh"]

EXPOSE 8000