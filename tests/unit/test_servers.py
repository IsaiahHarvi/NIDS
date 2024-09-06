import subprocess
import pytest
import os
import re
from icecream import ic


@pytest.fixture(scope="session")
def docker_compose():
    os.system("docker compose up --build -d")
    yield
    os.system("docker compose down")

@pytest.mark.slow()
def test_servers(docker_compose): # this is a temporary catchall
    os.system("python3 src/services/comms.py --test")
