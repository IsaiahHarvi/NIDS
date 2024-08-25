import os
from icecream import ic
# import pytest

def pytest_sessionstart(session):
    """
    Runs before every test session. Kills and removes all containers
    to free up any ports that would cause the test to fail otherwise.
    """
    ic("Killing and removing all existing services")
    os.system("docker kill $(docker ps -q) > /dev/null 2>&1")
    os.system("docker container prune -f > /dev/null 2>&1")
    os.system("docker image prune -f > /dev/null 2>&1")
