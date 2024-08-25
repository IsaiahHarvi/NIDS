import subprocess
import pytest
from icecream import ic

@pytest.fixture(scope="session")
def docker_compose():
    try:
        subprocess.run(
            ["docker", "compose", "up", "--build", "-d"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        yield
    finally:
        subprocess.run(
            ["docker", "compose", "down"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

def test_services(docker_compose):
    result = subprocess.run(
        ["docker", "compose", "ps"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode("utf-8")
    ic(output)
    assert "Exit" not in output, "One or more services failed to start."
    assert "Up" in output, "Services are not staying up."
