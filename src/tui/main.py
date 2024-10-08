import asyncio

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import Button, Footer, Header, RichLog, Static

from src.tui.utils import CSS, async_execute, execute


class NIDS(App):
    CSS = CSS
    BINDINGS = [
        ("ctrl+1", "feeder_logs", "Feeder Logs"),
        ("ctrl+2", "nn_logs", "Neural Network Logs"),
        ("ctrl+3", "webserver_logs", "GUI Logs"),
        ("ctrl+4", "all_logs", "All Logs"),
        ("ctrl+5", "clear_logs", "Clear"),
        ("ctrl+6", "health_check", "Healthchecks"),
    ]

    def __init__(self):
        super().__init__()
        self.compose_running: bool = False
        self.compose_up_button = Button("Start Components", id="compose_up")
        self.compose_down_button = Button("Stop Components", id="compose_down")
        self.output_log = RichLog(highlight=False, markup=False, id="output_log")
        self.log_tasks = {}

    def compose(self) -> ComposeResult:
        """Create the layout of the application."""
        yield Header(show_clock=True)
        yield Horizontal(
            self.compose_up_button,
            self.compose_down_button,
            Button("Kill Components", id="kill_components"),
            id="button",
        )
        yield Horizontal(
            Container(
                self.output_log,
                id="left"
            ),
            Container(
                Static(id="docker_ps", name="docker_ps_display"),
                RichLog(id="docker_logs", highlight=False),
                id="right",
            )
        )
        yield Footer()

    async def on_mount(self):
        """Run when the app starts."""
        asyncio.create_task(self.monitor_docker_ps())
        self.compose_down_button.disabled = True

    async def monitor_docker_ps(self):
        """Continuously run `docker ps` and update the display every 5 seconds."""
        while True:
            output, _ = execute('docker ps --format "table {{.ID}}\t{{.Status}}\t{{.Names}}"')
            compose_running = len(output.strip().splitlines()) > 1

            self.compose_up_button.disabled = compose_running
            self.compose_down_button.disabled = not compose_running
            self.query_one("#docker_ps", Static).update(output)
            await asyncio.sleep(5)
        
    async def monitor_docker_logs(self, container_name: str):
        """Fetch and stream logs for the selected container."""
        process = await asyncio.create_subprocess_shell(
            f'docker logs -f {container_name}',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        async def stream_logs(stream, is_stdout=True):
            """Stream logs continuously and write to the RichLog widget."""
            docker_logs_widget = self.query_one("#docker_logs", RichLog)
            while True:
                line = await stream.readline()
                if line:
                    output = line.decode().strip()
                    docker_logs_widget.write(output)
                else:
                    break

        await asyncio.gather(
            stream_logs(process.stdout),
            stream_logs(process.stderr)
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses."""
        match event.button.id:
            case "compose_up":
                if not self.compose_running:
                    asyncio.create_task(self.run_docker_compose())
            case "compose_down":
                asyncio.create_task(self.stop_docker_compose())
            case "kill_components":
                execute("docker kill $(docker ps -q)")

    async def run_docker_compose(self):
        """Run docker-compose up and display output in the TUI, with auto-scrolling."""
        self.set_compose(running=True)

        process = await asyncio.create_subprocess_shell(
            "docker compose --profile gui --profile feeder up --build -d",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            stdout_line = await process.stdout.readline()
            stderr_line = await process.stderr.readline()
            if stdout_line:
                output = stdout_line.decode().strip()
                self.output_log.write(output)
            if stderr_line:
                output = stderr_line.decode().strip()
                self.output_log.write(output)
            if not stdout_line and not stderr_line:
                break

    async def stop_docker_compose(self):
        self.set_compose(running=False)

        process = await asyncio.create_subprocess_shell(
            "docker compose down",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        while True:
            stdout_line = await process.stdout.readline()
            stderr_line = await process.stderr.readline()
            if stdout_line:
                output = stdout_line.decode().strip()
                self.output_log.write(output)
            if stderr_line:
                output = stderr_line.decode().strip()
                self.output_log.write(output)
            if not stdout_line and not stderr_line:
                break
    
    def action_feeder_logs(self):
        self.query_one("#docker_logs", RichLog).clear()
        self.start_log_task("feeder")
    
    def action_nn_logs(self):
        self.query_one("#docker_logs", RichLog).clear()
        self.start_log_task("neural-network")
 
    def action_webserver_logs(self):
        self.query_one("#docker_logs", RichLog).clear()
        self.start_log_task("webserver")
    
    def action_all_logs(self):
        self.query_one("#docker_logs", RichLog).clear()
        self.start_log_task("logger")

    def action_clear_logs(self):
        self.query_one("#docker_logs", RichLog).clear()

    async def action_health_check(self):
        """Run the health check asynchronously."""
        output, error = await async_execute("python src/services/comms.py --check --sleep 0")
        if output:
            self.output_log.write(output)
        if error:
            self.output_log.write(error)

    def start_log_task(self, container_name):
        """Start log streaming task for the container."""
        if container_name in self.log_tasks:
            self.log_tasks[container_name].cancel()

        task = asyncio.create_task(self.monitor_docker_logs(container_name))
        self.log_tasks[container_name] = task

    def set_compose(self, running: bool):
        self.compose_running = running
        self.compose_up_button.disabled = self.compose_running
        self.compose_down_button.disabled = not self.compose_running

if __name__ == "__main__":
    NIDS().run()
