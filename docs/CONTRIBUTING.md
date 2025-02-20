# Contributing to NIDS

Thank you for your interest in contributing to the NIDS repository! We welcome contributions from both internal collaborators and the broader public. Please follow the guidelines below based on your preferred development environment.

## Workflow

### For Internal Collaborators

1. **Branch Creation from an Issue:**
   - Navigate to the issue on the repository’s web interface.
   - Click the **"Create a branch"** (or similar) button on the issue page.
   - Copy and execute the provided commands locally to create and checkout the branch.

2. **Draft Pull Request:**
   - In the web interface, open a draft pull request (PR) from your branch.
      > **base:** main **←** **compare:** your-branch-name
   - Initially mark the PR as a **draft** to indicate it’s a work in progress.

3. **Develop Your Changes:**
   - Work on your branch, staging and committing changes frequently.

4. **Ready for Review:**
   - Once you’re finished with your changes and all tests pass, update the PR from draft status to ready for review.

---

### For Open Source Contributors

1. **Fork the Repository:**
   - Create a fork of the NIDS repository on GitHub.

2. **Branch Creation from an Issue:**
   - In your fork, navigate to the issue and click **"Create a branch"** to generate the branch creation commands.
   - Clone your fork locally and checkout the new branch.

3. **Develop Your Changes:**
   - Make your changes locally.
   - Stage and commit your updates:
     ```bash
     git add .
     git commit -m "Implement feature/fix issue #<issue-number>: brief description"
     ```
   - Push your branch to your fork:
     ```bash
     git push -u origin your-branch-name
     ```

4. **Draft Pull Request:**
   - Open a pull request from your branch in your fork to the main repository.
   - Mark it as a **draft** to signal that work is still in progress.

5. **Mark as Ready for Review:**
   - When your changes are complete and tested, update the pull request from draft status to ready for review.

## Guidelines

- **Pull Requests:** Ensure that your changes work in your chosen environment (remote or local) and are thoroughly tested before submitting a pull request.
- **Code Style:** All contributions must be ruff checked and formatted.
  > ruff check . && ruff format .
- **Documentation:** Update relevant documentation as needed when introducing new features or modifying existing ones.
- **Testing:** Include tests for new functionality whenever possible.

## Development Environments

### 1. Remote Server
- **Usage:** Collaborators with access to our remote server should use the `nids-cpu` environment.

### 2. Local Development using the Local-NIDS Devcontainer
- **Usage:** Public contributors, or collaborators who prefer a local workflow, can develop using the `local-nids` devcontainer.

Instructions for both environments are found in the [Development Setup Guide](setup.md)


## Need Help?
### Docker
[Common Commands for Development and Testing](docker.md)

### Ruff
[Linting and Formatting](ruff.md)

### Git
[Common Git Commands](git.md)

If you have other questions or encounter issues, please open an issue in the repository or reach out to the maintainers.
