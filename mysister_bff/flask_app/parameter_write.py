from flask_app import sound_device
#import main
import sys
sys.dont_write_bytecode = True
from flask_app.setup_logger import setup_logger
import threading
sys.path.append("../config")
import conf
#import dynamic_property
import configparser

class parameter_write:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read("./flask_app/dynamic_property.ini")
        self.logger = setup_logger(__name__)
        self.logger.info("parameter write init")

    def service(self, request):
        parameter = request.form.to_dict()

        print(self.config.sections()) 

        self.config["BASE"]["mode_num"] = parameter["mode"]
        self.config["BASE"]["device"]   = parameter["device"]
        self.config["BASE"]["status"]   = "start"

        with open("./flask_app/dynamic_property.ini", "w") as file:
            self.config.write(file)


