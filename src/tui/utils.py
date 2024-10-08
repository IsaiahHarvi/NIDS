import asyncio
import os
import subprocess


def execute(command):
    """Run a command and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
        return result.stdout, result.stderr
    except Exception as e:
        output = f"Error: {str(e)}"
    return output

async def async_execute(command: str):
    """Run a shell command asynchronously."""
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()

BINDINGS = [
    ("ctrl+1", "feeder_logs", "Feeder Logs"),
    ("ctrl+2", "nn_logs", "Neural Network Logs"),
    ("ctrl+3", "webserver_logs", "GUI Logs"),
    ("ctrl+4", "all_logs", "All Logs"),
    ("ctrl+5", "clear_terminal", "Clear Terminal"),
    ("ctrl+6", "clear_logs", "Clear Logs"),
    ("ctrl+7", "health_check", "Healthchecks"),
]

CSS = """
Button {
    width: 25%;
    margin: 1 0;
    color: white;
    background: black;
    outline: heavy white;
}

RichLog#output_log {
    background: black;
    color: white;
    padding: 1;
    border: heavy white;
    overflow: auto;
}

Static#docker_ps {
    background: black;
    border: heavy white;
    color: white;
    padding: 1;
    height: 50%;
}

RichLog#docker_logs {
    background: black;
    border: heavy white;
    color: white;
    padding: 1;
    height: 50%;
}

Container#left {
    width: 50%;
    background: black;
}

Container#right {
    width: 50%;
    background: black;
}

Container#button {
    overflow-x: auto;
    background: black;
    width: 50%;
    height: 30%;
}

Horizontal {
    height: auto;
}
"""
