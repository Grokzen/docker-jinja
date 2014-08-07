import os


def _global_env_var_is(key, value):
    """
    Check if file exists on disk or not.
    """
    if key not in os.environ:
        return False
    else:
        return os.environ[key] == value
