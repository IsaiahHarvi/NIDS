import subprocess
import pytest
import os
import re
from time import sleep
from icecream import ic
from tests.conftest import compose


def get_image_names() -> list[str]:
    image_names = []
    for root, _, files in os.walk("deploy"):
        for file in files:
            if file == "compose.yml":
                file_path = os.path.join(root, file)
                with open(file_path, "r") as f:
                    image_names.extend(
                        re.findall(r"image:\s*([\w\/\:\.\-]+)", f.read())
                    )
    return image_names

def test_services(compose):
    result = subprocess.run(
        ["docker", "compose", "ps"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = result.stdout.decode("utf-8")
    print(output)
    sleep(2)
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
