import subprocess
import sys

import pytest

from tests.conftest import compose


@pytest.mark.slow()
def test_servers(compose):
    result = subprocess.run(
            ["python3", "src/services/comms.py", "--test"], text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    assert "Error" not in result.stdout # dumb
