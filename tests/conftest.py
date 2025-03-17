import os
import subprocess

import pytest
from icecream import ic

# import pytest


def pytest_sessionstart(session):
    """
    Runs before every test session. Kills all containers
    to free up any ports that would cause the test to fail otherwise.
    """
    os.system("docker kill $(docker ps --filter 'name=nids-' -q) > /dev/null 2>&1")

@pytest.fixture(scope="session")
def compose():
    """
    Fixture that runs docker compose up, yields, and then brings the services down.
    """
    subprocess.run(
        ["docker", "compose", "up", "--build", "-d"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
    yield
    subprocess.run(
        ["docker", "compose", "down"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE
    )
