# Chromecast MQTT-smarthome connector

Fork of [nohum](https://github.com/nohum)'s [chromecast-mqtt-connector](https://github.com/nohum/chromecast-mqtt-connector) using topic naming convetion from [mqtt-smarthome](https://github.com/mqtt-smarthome/mqtt-smarthome).

## Usage

	git clone 
	pip3 install -r requirements.txt
	cp config.ini.dist config.ini
	nano config.ini
	python3 connector.py

## Docker

Create a `config.ini` with your settings and run with:

	docker run -d --net=host -v $(pwd)/config.ini:/python/config.ini dersimn/chromecast-mqtt-smarthome-connector
	docker run -d --net=host -v $(pwd)/config.ini:/python/config.ini dersimn/chromecast-mqtt-smarthome-connector:armhf

## Discovery and control

Using MQTT you can find the following topics. `friendly_name` is the name used to connect
to each Chromecast.

	chromecast/status/FRIENDLY_NAME/friendly_name
	chromecast/status/FRIENDLY_NAME/connection_status
	chromecast/status/FRIENDLY_NAME/cast_type
	chromecast/status/FRIENDLY_NAME/current_app
	chromecast/status/FRIENDLY_NAME/player_duration
	chromecast/status/FRIENDLY_NAME/player_position
	chromecast/set   /FRIENDLY_NAME/player_position
	chromecast/status/FRIENDLY_NAME/player_state
	chromecast/set   /FRIENDLY_NAME/player_state
	chromecast/status/FRIENDLY_NAME/volume_level
	chromecast/set   /FRIENDLY_NAME/volume_level
	chromecast/status/FRIENDLY_NAME/volume_muted
	chromecast/set   /FRIENDLY_NAME/volume_muted
	chromecast/status/FRIENDLY_NAME/media/title
	chromecast/status/FRIENDLY_NAME/media/album_name
	chromecast/status/FRIENDLY_NAME/media/artist
	chromecast/status/FRIENDLY_NAME/media/album_artist
	chromecast/status/FRIENDLY_NAME/media/track
	chromecast/status/FRIENDLY_NAME/media/images
	chromecast/status/FRIENDLY_NAME/media/content_type
	chromecast/status/FRIENDLY_NAME/media/content_url

Change volume using values from `0` to `100`:

* Absolute: publish e.g. `55` to `chromecast/friendly_name/command/volume_level`
* Relative: publish e.g. `+5` or `-5` to `chromecast/friendly_name/command/volume_level`

Change mute state: publish `0` or `1` to `chromecast/friendly_name/command/volume_muted`.

Play something: Publish a json array with two elements (content url and content type) to
`chromecast/friendly_name/command/player_state`, e.g. `["http://your.stream.url.here", "audio/mpeg"]`.
You can also just publish a URL to `player_state` (just as string, not as json array, e.g.
`http://your.stream.url.here`), the application then tries to guess the required MIME type.

For other player controls, simply publish e.g. `RESUME`, `PAUSE`, `STOP`, `SKIP` or `REWIND` to
`chromecast/friendly_name/command/player_state`. Attention: This is case-sensitive!

## Development / Debug

### docker build

	docker build -t chromecast-mqtt-smarthome-connector .
	docker build -t chromecast-mqtt-smarthome-connector:armhf -f Dockerfile.armhf .
