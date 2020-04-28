from paho.mqtt.client import Client, MQTT_ERR_NO_CONN, MQTT_ERR_SUCCESS
import logging


class MqttConnectionCallback:

    def on_mqtt_connected(self, client):
        pass

    def on_mqtt_message_received(self, topic, payload):
        pass


class MqttConnection:

    def __init__(self, ip, port, username, password, cafile, connection_callback):
        self.logger = logging.getLogger("mqtt")

        self.mqtt = Client()
        if username is not None:
            self.mqtt.username_pw_set(username, password)

        if cafile is not None:
            self.mqtt.tls_set(ca_certs=cafile)

        self.mqtt.will_set("chromecast/maintenance/_bridge/online", payload="false", retain=True)

        self.mqtt.on_connect = self._on_connect
        self.mqtt.on_message = self._on_message

        self.ip = ip
        self.port = int(port)
        self.connection_callback = connection_callback
        self.queue = []

    def _on_connect(self, client, userdata, flags, rc):
        """
        The callback for when the client receives a CONNACK response from the server.
        """
        self.logger.debug("connected to mqtt with result code %d" % rc)
        self.mqtt.publish("chromecast/maintenance/_bridge/online", "true", retain=True)

        # subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.connection_callback.on_mqtt_connected(self)

        if len(self.queue) > 0:
            self.logger.debug("found %d queued messages" % len(self.queue))
            for msg in self.queue:
                self._internal_send_message(msg[0], msg[1], False)

            self.queue.clear()
            self.logger.debug("handled all queued messages")

    def _on_message(self, client, userdata, msg):
        """
        The callback for when a PUBLISH message is received from the server.
        """
        self.logger.debug("received mqtt publish of %s with data \"%s\"" % (msg.topic, msg.payload))
        self.connection_callback.on_mqtt_message_received(msg.topic, msg.payload)

    def send_message(self, topic, payload):
        return self._internal_send_message(topic, payload, True)

    def subscribe(self, topic):
        self.logger.debug("subscribing to topic %s" % topic)
        result = self.mqtt.subscribe(topic)

        if result[0] == MQTT_ERR_NO_CONN:
            self.logger.warning("no connection while trying to subscribe to topic %s" % topic)
            return False

        return result[0] == MQTT_ERR_SUCCESS

    def unsubscribe(self, topic):
        self.logger.debug("unsubscribing from topic %s" % topic)
        result = self.mqtt.unsubscribe(topic)

        if result[0] == MQTT_ERR_NO_CONN:
            self.logger.warning("no connection while trying to unsubscribe from topic %s" % topic)
            return False

        return result[0] == MQTT_ERR_SUCCESS

    def _internal_send_message(self, topic, payload, queue):
        self.logger.debug("sending topic %s with value \"%s\"" % (topic, payload))
        result = self.mqtt.publish(topic, payload, retain=True)

        if result == MQTT_ERR_NO_CONN and queue:
            self.logger.debug("no connection, saving message with topic %s to queue" % topic)
            self.queue.append([topic, payload])
        elif result[0] != MQTT_ERR_SUCCESS:
            self.logger.warn("failed sending message %s, mqtt error %s" % (topic, result))
            return False

        return True

    def start_connection(self):
        try:
            self.mqtt.connect(self.ip, self.port)
        except ConnectionError:
            self.logger.exception("failed connecting to mqtt")
            return False

        self.mqtt.loop_start()
        return True

    def stop_connection(self):
        self.mqtt.publish("chromecast/maintenance/_bridge/online", "false", retain=True)
        self.mqtt.disconnect()
        self.mqtt.loop_stop()
