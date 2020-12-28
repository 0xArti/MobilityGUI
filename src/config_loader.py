import os
import json
import base64
from pathlib import Path


class DynamicConfig():
    """
    Dynamic config class from configuration file.
    Creates attribute for keys and set method for their values
    Also acts as a dict

    Example usage:
        config = DynamicConfig(a=1, b="bird")

        config.a = 2
        print(config.a)

        config.set_b("dog")
        print(config.b)

        config["c"] = "new"

        for key, value in config.items():
            print(config[key])

    """
    def __init__(self, **options):
        for key, value in options.items():
            self.__set_key(key, value)
            self.__create_setter(key)

    def __set_key(self, key, value):
        self.__setattr__(key, value)

    def __create_setter(self, key):
        setattr(self.__class__, f"set_{key}", self.__set_value(key))

    def __set_value(self, key, value=None):
        def __inner(self, value):
            self.__set_key(key, value)
        return __inner
    
    def __setitem__(self, key, item):
        if not hasattr(self, key):
            self.__create_setter(key)
        self.__set_key(key, item)

    def __getitem__(self, key):
        return getattr(self, key)

    def items(self):
        return self.__dict__.items()


def get_path(*args):
    """
    Cross-Platform path to file function
    """
    return Path(os.path.dirname(__file__), *args)


def load_from_configuration(file_name, key=None):
    """
    Returns the configuration of the specified file
    Optional: configuration key - returns the sub-config value
    """
    config_path = get_path("..", "configuration", file_name)
    with open(config_path, "r") as config_handler:
        config = json.load(config_handler)
        if key:
            config = config[key]
    return config


def load_from_assets(file_name):
    """
    Returns the base64 value of the specified file from the assets
    """
    image_path = get_path("..", "assets", file_name)
    with open(image_path, "rb") as image_handler:
        return base64.b64encode(image_handler.read())


