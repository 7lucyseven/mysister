import sound_device
#import main
import sys
sys.dont_write_bytecode = True
#import mysister
from setup_logger import setup_logger
import threading
sys.path.append("../config")
import conf
#import dynamic_property
import configparser

class parameter_write:
    config = configparser.ConfigParser()
    config.read("dynamic_property.ini")

def service(request):
    parameter = request.form.to_dict()

    parameter_write.config["BASE"]["mode_num"] = parameter["mode"]
    parameter_write.config["BASE"]["device"]   = parameter["device"]
    parameter_write.config["BASE"]["status"]   = "start"

    with open("dynamic_property.ini", "w") as file:
        parameter_write.config.write(file)

    return "test"



