import configparser
import os

class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = "/config/config.ini"

        if not self._test_config_file(self.config_file):
            # try the dist file instead
            self.config_file = "/config/config.ini.dist"
            dist_works = self._test_config_file(self.config_file)

            if not dist_works:
                raise Exception("could not find any config file")

        # Parse what we've found
        self.config.read(self.config_file)

        if 'mqtt' not in self.config.sections():
            raise Exception("incorrect configuration format!")

    def _test_config_file(self, config_file):
        exists = os.access(config_file, os.F_OK)
        readable = os.access(config_file, os.R_OK)
        return exists and readable

    def get_mqtt_broker_address(self):
        return self.config['mqtt']['broker_address']

    def get_mqtt_broker_port(self):
        return self.config['mqtt']['broker_port']

    def get_mqtt_broker_use_auth(self):
        return self.config['mqtt']['use_auth']

    def get_mqtt_broker_username(self):
        return self.config['mqtt']['username']

    def get_mqtt_broker_password(self):
        return self.config['mqtt']['password']

    def get_mqtt_client_cafile(self):
        # I should fix this
        return None
