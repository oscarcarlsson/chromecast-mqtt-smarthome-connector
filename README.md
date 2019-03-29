# Chromecast MQTT-smarthome connector

Fork of [nohum](https://github.com/nohum)'s [chromecast-mqtt-connector](https://github.com/nohum/chromecast-mqtt-connector) using topic naming convetion from [mqtt-smarthome](https://github.com/mqtt-smarthome/mqtt-smarthome).

## Usage

Control behaviour by defining ENV variables `MQTT_HOST`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASSWORD`, `MQTT_CAFILE`.

	git clone 
	pip3 install -r requirements.txt
	MQTT_HOST=10.1.1.50 python3 connector.py

## Docker

	docker run -d --net=host -e "MQTT_HOST=10.1.1.100" dersimn/chromecast-mqtt-smarthome-connector

## Discovery and control

Using MQTT you can find the following topics. `FRIENDLY_NAME` is the name used to connect
to each Chromecast.

	chromecast/maintenance/_bridge/online -> bool

	chromecast/maintenance/FRIENDLY_NAME/online -> bool
	chromecast/maintenance/FRIENDLY_NAME/connection_status -> string
	chromecast/maintenance/FRIENDLY_NAME/cast_type -> string

	chromecast/status/FRIENDLY_NAME/current_app -> string

	chromecast/status/FRIENDLY_NAME/volume -> JSON
	chromecast/set   /FRIENDLY_NAME/volume -> float
	chromecast/set   /FRIENDLY_NAME/volume/muted -> bool

	chromecast/status/FRIENDLY_NAME/player -> JSON
	chromecast/set   /FRIENDLY_NAME/player -> string
	chromecast/set   /FRIENDLY_NAME/player/position -> int

	chromecast/status/FRIENDLY_NAME/media -> JSON

Change volume using values from `0` to `1.0`:

* Publish e.g. `1.0` to `chromecast/set/FRIENDLY_NAME/volume`

Change mute state: publish `false` or `true` to `chromecast/set/FRIENDLY_NAME/volume/muted`.

Play something: Publish a json array with two elements (content url and content type) to
`chromecast/set/FRIENDLY_NAME/player`, e.g. `["http://your.stream.url.here", "audio/mpeg"]`.
You can also just publish a URL to `player_state` (just as string, not as json array, e.g.
`http://your.stream.url.here`), the application then tries to guess the required MIME type.

For other player controls, simply publish e.g. `RESUME`, `PAUSE`, `STOP`, `SKIP` or `REWIND` to
`chromecast/set/FRIENDLY_NAME/player`. Attention: This is case-sensitive!

## Development / Debug

### docker build

	docker build -t chromecast-mqtt-smarthome-connector .

Raspberry Pi:

	docker pull --platform arm arm32v7/python:3
	docker build -t chromecast-mqtt-smarthome-connector:armhf -f Dockerfile.armhf .
