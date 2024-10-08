import os
import subprocess


def execute(command):
    """Run a command and return the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, env=os.environ)
        output = result.stdout
        return result.stdout, result.stderr
    except Exception as e:
        output = f"Error: {str(e)}"
    return output

CSS = """
    Button {
        width: 80%;
        margin: 1 0;
        color: white;
        background: dimgrey;
        outline: darkgrey;
    }
    RichLog#output_log {
        color: white;
        padding: 1;
        border: heavy darkslategray;
        overflow: auto;
    }
    Static#docker_ps {
        background: darkslategray;
        color: white;
        padding: 1;
        border: hkey white;
        height: 50%;
    }
    Static#docker_logs {
        background: darkslategray;
        color: white;
        padding: 1;
        border: hkey white;
        height: 50%;
    }
    Container#left {
        width: 50%;
        border: heavy white;
    }
    Container#right {
        width: 50%;
        border: heavy white;
    }
    Horizontal {
        height: auto;
    }
"""
