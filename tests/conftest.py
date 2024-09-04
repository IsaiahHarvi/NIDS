import os
from icecream import ic

# import pytest


def pytest_sessionstart(session):
    """
    Runs before every test session. Kills all containers
    to free up any ports that would cause the test to fail otherwise.
    """
    os.system("docker kill $(docker ps -q) > /dev/null 2>&1")
