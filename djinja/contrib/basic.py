import os


def _global_env_var_is(key, value):
    """
    Check if file exists on disk or not.
    """
    return os.environ[key] == value
