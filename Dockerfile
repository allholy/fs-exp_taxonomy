FROM python:3.10

RUN wget -O /usr/local/bin/dumb-init https://github.com/Yelp/dumb-init/releases/download/v1.2.2/dumb-init_1.2.2_amd64 \
    && chmod +x /usr/local/bin/dumb-init

RUN mkdir /code
ADD requirements.txt /code

WORKDIR /code
RUN pip install --no-cache-dir -r requirements.txt

ADD . /code

ENV PYTHONUNBUFFERED=1