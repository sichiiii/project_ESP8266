import network, esp, serial
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
        self.params = self.config.get('ESP', 'params')
        self.port_name = self.config.get('ESP', 'port')
        self.baudrate = self.config.get('ESP', 'baudrate')
        self.pause = self.config.get('ESP', 'pause')
        self.ser = serial.Serial(self.port_name, self.baudrate, timeout=int(self.pause)) 
    
    def check(self):
        try:
            data = self.ser.readline().decode("utf-8")
            final_string = ''
            for i in data:
                final_string = final_string + i
            return data
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}

    def update_ports(self):    #TODO: Обновлять значения. которые будут в базе
        try:
            return 'Building...'
        except Exception as ex:
            self.logger.error(str(ex))
            return {'status':'error'}