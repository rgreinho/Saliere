from os import path
import yaml

from saliere.core import ConfigError
from saliere.core import FileNotFoundError


class Config:
    """The configuration manager.

    Read the configuration values from a yaml file.
    """

    def __init__(self):
        # Initialize the configuration with default values
        self.config = {
            'template_path': [
                'data/template',
                '../data/template',
                '/usr/local/share/saliere/templates'
            ]
        }  # yapf: disable

    def load_from_string(self, yaml_string):
        """Load the configuration from a YAML string.

        :param yaml_string:
        :return:
        """
        try:
            self.config.update(yaml.load(yaml_string))
        except Exception as e:
            # Failed yaml loading? Stop here!
            raise ConfigError("Config is not valid yaml ({0}): \n{1}".format(e, yaml_string))

    def load_from_file(self, config_file=None):
        """

        :param config_file:
        :return:
        """
        file_content = ""

        # If a configuration file was provided...
        if config_file:
            # ..ensure it exists.
            if not path.exists(config_file):
                raise FileNotFoundError("")

            # Read the configuration file.
            try:
                with open(config_file, mode='r', encoding='utf-8') as configuration_file:
                    file_content = configuration_file.read()
            except:
                raise ConfigError("Cannot read the configuration file '{}'".format(config_file))

        # Load the configuration file.
        self.load_from_string(file_content)

    def get_value(self, key, default=None, silent_fail=True):
        """Retrieves a value matching a key in the config file.

        :param key: the key to look for
        :param default: the default value to return if the key is not found
        :param silent_fail: if true, returns the default value if the key is not found, otherwise raises an exception
        :return: the value matching the key
        """
        # Ensure we have a configuration.
        if not self.config:
            raise ConfigError("No configuration was loaded. Check your configuration file.")

        # Ensure a key was provided.
        if not key:
            raise ConfigError("Invalid key: '{}'.".format(key))

        # Split the keys.
        key_list = key.split(':')

        # Create a copy of the configuration to iterate through it.
        dict_conf = self.config

        for dict_key in key_list:
            # Retrieve the value of the key in the configuration file.
            value = dict_conf.get(dict_key)

            # Keep iterating if there is value.
            if value:
                dict_conf = value
            else:
                break

        # Return the value matching the key if we found it.
        if value:
            return value
        else:
            # Otherwise return the default value.
            if silent_fail:
                return default

            # Or raise an exception.
            raise ConfigError("Configuration key {0} not found in the request payload.".format(key))
