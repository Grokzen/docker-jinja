import os


def _global_file_exists(path):
    """
    Check if file exists on disk or not.
    """
    return os.path.exists(path)
