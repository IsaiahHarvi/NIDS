import subprocess
import pytest
import os

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

def test_docker_services(docker_compose):
    """Test that the Docker services are up and running."""
    result = subprocess.run(
        ["docker", "compose", "ps"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output = result.stdout.decode("utf-8")

    assert "Exit" not in output, "One or more services failed to start."
    assert "Up" in output, "Services are not staying up."
