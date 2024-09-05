import subprocess
import pytest
import os
import re
from icecream import ic


@pytest.fixture(scope="session")
def docker_compose():
    try:
        subprocess.run(
            ["docker", "compose", "up", "--build", "-d"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        yield
    finally:
        subprocess.run(
            ["docker", "compose", "down"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

def get_image_names() -> list[str]:
    image_names = []
    for root, dirs, files in os.walk("deploy"):
        for file in files:
            if file == "compose.yml":
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    image_names.extend(
                        re.findall(r"image:\s*([\w\/\:\.\-]+)", f.read())
                    )
    return image_names

def test_services(docker_compose):
    result = subprocess.run(
        ["docker", "compose", "ps"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = result.stdout.decode("utf-8")
    print(output)
    assert "Exit" not in output, "One or more services failed to start."
    assert "Up" in output, "Services are not staying up."

    # # Get all service names currently running
    # running_service_names = (
    #     subprocess.run(
    #         ["docker", "compose", "ps", "--format", "{{.Names}}"],
    #         stdout=subprocess.PIPE,
    #         stderr=subprocess.PIPE,
    #         text=True,
    #     )
    #     .stdout.strip()
    #     .split("\n")
    # )

    # # Get expected services by counting image names in all compose files
    # expected_service_images = get_image_names()
    # ic(expected_service_images)
    # ic(running_service_names)

    # assert len(expected_service_images) == len(
    #     running_service_names
    # ), f"Expected {len(expected_service_images)} services, but found {len(running_service_names)} running."
