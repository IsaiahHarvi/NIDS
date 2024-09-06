import subprocess
import sys
import pytest
from tests.conftest import compose


@pytest.mark.slow()
def test_servers(compose):
    result = subprocess.run(
        ["python3", "src/services/comms.py", "--test"],
        text=True,
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
    assert result.returncode == 0
