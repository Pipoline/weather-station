FROM python:3-alpine

MAINTAINER Peter Gonda <peter@pipoline.com>

ARG repo=test
ARG token=test

RUN apk -U add zlib-dev jpeg-dev gcc build-base linux-headers nginx \
    && rm -rf /var/cache/apk/* \
    && pip install uwsgi

ADD nginx.conf /etc/nginx/nginx.conf
ADD uwsgi.ini /etc/uwsgi.ini

WORKDIR /srv
ADD requirements.txt /srv/
RUN pip install -r requirements.txt

EXPOSE 80
STOPSIGNAL SIGQUIT

ADD docker-entrypoint.sh /root
RUN chmod 700 /root/docker-entrypoint.sh

ADD . /srv

CMD ["/root/docker-entrypoint.sh"]
