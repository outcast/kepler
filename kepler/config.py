import yaml
import argparse


class Config(object):
    def __init__(self, config_file_path):
        self._config_file_path = config_file_path
        self.config = self._load()

    def _load(self):
        config_yaml = open(self._config_file_path)
        config = yaml.load(config_yaml)
        config_yaml.close()
        return config

"""
parser = argparse.ArgumentParser(description='Kepler Server')
parser.add_argument('config_file_path',help="Path to config file")
args = parser.parse_args()
"""

config = Config("./config/config.yaml").config
