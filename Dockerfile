FROM selenium/standalone-chrome:122.0-chromedriver-122.0

USER root
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get install -y  git

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip3 install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./ /code/app

WORKDIR /code/app

CMD ["python3", "app/main.py"]