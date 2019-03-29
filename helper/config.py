import os


class Config:

    def __init__(self):
        self.addr = os.getenv('MQTT_HOST', '127.0.0.1')
        self.port = int(os.getenv('MQTT_PORT', 1883))
        self.user = os.getenv('MQTT_USER', False)
        self.password = os.getenv('MQTT_PASSWORD', False)
        self.cafile = os.getenv('MQTT_CAFILE', None)

    def get_mqtt_broker_address(self):
        return self.addr

    def get_mqtt_broker_port(self):
        return self.port

    def get_mqtt_broker_use_auth(self):
        return (self.user and self.password)

    def get_mqtt_broker_username(self):
        return self.user

    def get_mqtt_broker_password(self):
        return self.password

    def get_mqtt_client_cafile(self):
        return self.cafile
