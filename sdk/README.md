# SDK for Integration into NIDS

This SDK is designed to facilitate the integration of Docker components into NIDS. By leveraging modular utilities and streamlined workflows, it simplifies the development and deployment of NIDS-related services.

---

## Project Structure

The SDK provides a well-structured directory inside of the main NIDS project to ensure seamless integration. A crucial component of this is the `src/grpc/utils/` directory, which houses essential gRPC utilities for inter-service communication in NIDS environments.

### Key Directory: `src/grpc/utils/`
This directory includes:
- **gRPC Helpers**: Pre-built utilities to handle communication between services in the NIDS framework.

---

## Starting the SDK

To launch components developed with the SDK, use the following Docker Compose command:

```bash
docker compose --profile gui --profile sdk up --build
```

### Command Breakdown:
- `--profile SDK`: Starts only the services defined under the `SDK` profile in the `sdk/compose.yml` file.
- Ensure the NIDS services and dependencies are correctly configured before starting.

---

## Features
- **NIDS Focused Utilities**: Tailored for NIDS requirements with support for high-throughput data and real-time analysis.
- **gRPC Communication**: Seamless inter-service communication using tools in `src/grpc/utils/`.

---

For further details or assistance with integration, refer to the source code documentation.
