FROM python:3

RUN mkdir /config
RUN chmod 644 /config
VOLUME /config

COPY . /python

RUN cd /python && \
	pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "/python/connector.py" ]
