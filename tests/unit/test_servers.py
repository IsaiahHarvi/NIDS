import subprocess
import pytest
from tests.conftest import compose


@pytest.mark.slow()
def test_servers(compose):
   result = subprocess.run(
        ["python3", "src/services/comms.py", "--test"], capture_output=True, text=True
    )
   assert "Error" not in result.stdout # dumb
