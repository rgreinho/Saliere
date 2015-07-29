import copy


class UnspecifiedError(Exception):

    """Base class for all exceptions in docker_registry."""

    def __init__(self, *args, **kwargs):
        self.message = kwargs.pop('message', 'No details')
        super(UnspecifiedError, self).__init__(*args, **kwargs)


class UsageError(UnspecifiedError):
    """Exceptions related to use of the library.

    Missing files, wrong argument type, etc.
    """


class NotImplementedError(UsageError):
    """The requested feature is not supported / not implemented."""


class FileNotFoundError(UsageError):
    """The requested (config) file is missing."""


class WrongArgumentsError(UsageError):
    """Expected arguments type not satisfied."""


class ConfigError(UsageError):
    """The provided configuration has problems."""


class ConnectionError(UnspecifiedError):
    """Network communication related errors all inherit this."""


class UnreachableError(ConnectionError):
    """The requested server is not reachable."""


class MissingError(ConnectionError):
    """The requested ressource is not to be found on the server."""


class BrokenError(ConnectionError):
    """Something died on our hands, that the server couldn't digest..."""


def merge_dicts(a, b, raise_conflicts=False, path=None):
    """
    Merges the values of B into A.

    If the raise_conflicts flag is set to True, a LookupError will be raised if the keys are conflicting.

    :param a: the target dictionary
    :param b: the dictionary to import
    :param raise_conflicts: flag to raise an exception if two keys are colliding
    :param path: the dictionary path. Used to show where the keys are conflicting when an exception is raised.
    :return: The dictionary A with the values of the dictionary B merged into it.
    """
    # Set path.
    if path is None:
        path = []

    # Go through the keys of the 2 dictionaries.
    for key in b:
        # If the key exist in both dictionary, check whether we must update or not.
        if key in a:
            # Dig deeper for keys that have dictionary values.
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(a[key], b[key], raise_conflicts=raise_conflicts, path=(path + [str(key)]))

            # Skip the identical values.
            elif a[key] == b[key]:
                pass
            else:
                # Otherwise raise an error if the same keys have different values.
                if raise_conflicts:
                    raise LookupError("Conflict at '{path}'".format(path='.'.join(path + [str(key)])))

                # Or replace the value of A with the value of B.
                a[key] = b[key]
        else:
            # If the key does not exist in A, import it.
            a[key] = copy.deepcopy(b[key]) if isinstance(b[key], dict) else b[key]

    return a
