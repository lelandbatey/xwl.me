
FROM ubuntu

RUN apt-get update && \
  apt-get install -y python \
  python-pip \
  python-dev \
  libxml2-dev \
  libxslt-dev \
  gcc \
  make \
  && pip install virtualenv

WORKDIR /app

ENV XWL_DB_PATH /dbpath/src_url_database.sqlite3

COPY . /app
RUN virtualenv /env && /env/bin/pip install -r /app/requirements.txt
EXPOSE 5000

CMD ["/app/docker_entrypoint.sh"]
