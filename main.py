import network
from config import Configuration 
import app_logger

config_path = './config.ini'

class ESP():
    def __init__(self):
        self.logger = app_logger.get_logger(__name__)
        self.config = Configuration()
        self.config.load(config_path)
        self.essid = self.config.get('ESP', 'essid')
        self.password = self.config.get('ESP', 'password')

    def connect(self):
        try:
            sta_if = network.WLAN(network.STA_IF)
            sta_if.active(True)
            sta_if.connect(self.essid, self.password)
            sta_if.isconnected()
            sta_if.ifconfig()
        except Exception as ex:
            self.logger.error(str(ex))
