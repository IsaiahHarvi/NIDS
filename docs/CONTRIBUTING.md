# Contributing to NIDS

Thank you for your interest in contributing to the NIDS repository! We welcome contributions from both internal collaborators and the broader public. Please follow the guidelines below based on your preferred development environment.

## Development Environments

### 1. Remote Server
- **Usage:** Collaborators with access to our remote server should use the `nids-cpu` environment.
 > **IMPORTANT:** When working on the remote server, **do not** run `scripts/update_docker_daemon.py`

### 2. Local Development using the Local-NIDS Devcontainer
- **Usage:** Public contributors, or collaborators who prefer a local workflow, can develop using the `local-nids` devcontainer.
- **Setup:**
  1. Clone the repository.
  2. **Important:** Before starting the devcontainer, run the Python script `scripts/update_docker_daemon.py` to set up your own local Docker registry.
  2. Open the repository in your devcontainer environment.
- **Warning:** This script is **only for local development** and **should not** be ran in SSH.

## Local Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone git@github.com:IsaiahHarvi/NIDS.git
   cd nids
   ```

2. **Run the Local Registry Setup Script**
   - Make sure you have the necessary administrative privileges.
   - Execute the script:
     ```bash
     python3 scripts/update_docker_daemon.py
     ```
   - This script updates your Docker daemon configuration to add the insecure registry required for local development.

3. **Open in Devcontainer**
   - Use your preferred development tool (e.g., VS Code with the Remote - Containers extension) to open the repository in the `local-nids` devcontainer.

## Remote Setup Instructions
Inside of Vscode:
   ```bash
   CTRL+SHIFT+P > Reopen current window in ssh
   git clone git@github.com:IsaiahHarvi/NIDS.git
   Open folder /home/username/NIDS
   CTRL+SHIFT+P > Remote-Containers: Reopen in Container
   ```

## Additional Contributing Guidelines

- **Pull Requests:** Ensure that your changes work in your chosen environment (remote or local) and are thoroughly tested before submitting a pull request.
- **Code Style:** All contributions must be ruff checked and formatted.
  > ruff check . && ruff format .
- **Documentation:** Update relevant documentation as needed when introducing new features or modifying existing ones.
- **Testing:** Include tests for new functionality whenever possible.

## Need Help?

If you have questions or encounter issues, please open an issue in the repository or reach out to the maintainers.
