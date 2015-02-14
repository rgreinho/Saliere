import yaml

from saliere.core import ConfigError


class Config:
    """The configuration manager.

    Read the configuration values from a yaml file.
    """

    def __init__(self, config_file):
        try:
            self._config = yaml.load(config_file)
        except Exception as e:
            # Failed yaml loading? Stop here!
            raise ConfigError("Config is not valid yaml ({0}): \n{1}".format(e, config_file))

    def get_value(self, key, default=None, silent_fail=True):
        """Retrieves a value matching a key in the config file.

        :param key: the key to look for
        :param default: the default value to return if the key is not found
        :param silent_fail: if true, returns the default value if the key is not found, otherwise raises an exception
        :return: the value matching the key
        """
        # Ensure we have a configuration.
        if not self._config:
            raise ConfigError("No configuration was loaded. Check your configuration file.")

        # Split the keys.
        key_list = key.split(':')

        # Create a copy of the configuration to iterate through it.
        dict_conf = self._config

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
