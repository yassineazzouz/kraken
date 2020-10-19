import json
import logging as lg
import os

_logger = lg.getLogger(__name__)


class FileSystemsConfig(object):
    config_file = "filesystems.json"
    default_conf_dir = os.path.expanduser("/etc/kraken/conf")

    def __init__(self, path=None):
        self._filesystems = {}

        self.conf_dir = path or os.getenv("KRAKEN_CONF_DIR", self.default_conf_dir)
        self.conf_file = os.path.join(self.conf_dir, self.config_file)

        if os.path.exists(self.conf_file):
            try:
                self.config = json.loads(open(self.conf_file).read())
            except Exception as e:
                raise KrakenConfigurationException(
                    "Exception while loading configuration file %s.", self.conf_file, e
                )

            _logger.info("Instantiated configuration from %s.", self.conf_file)
        else:
            return None

    def get_config(self):
        return self.config


class KrakenConfigurationException(Exception):
    pass
