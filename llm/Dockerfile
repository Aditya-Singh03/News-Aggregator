FROM python:3.12-slim

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt update -y 
RUN apt-get install libpq-dev python3-dev wget g++ gcc -y

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY requirements_test.txt .
RUN pip3 install -r requirements_test.txt

COPY . .
EXPOSE 8040

CMD [ "python", "main.py" ]