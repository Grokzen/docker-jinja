# coding=utf-8
"""
This must exists for py.test to work out the path to 'ed' folder
"""

# djinja package imports
from djinja import _local_env

# 3rd party imports
import pytest


@pytest.fixture(autouse=True)
def reset_jinja(request):
    """
    Reset global _local_env variable between each test to ensure clean state
    """
    global _local_env

    _local_env = {
        "global": {},
        "filters": {}
    }
