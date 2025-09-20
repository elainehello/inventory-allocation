# Allocation Service

This repository contains the implementation of an allocation service, designed using a clean architecture approach. The service is responsible for managing stock allocation, handling domain events, and integrating with external systems.

## Project Structure

The project is organized into the following layers and directories:

```
src/
├── allocation/
    ├── config/                     # Configuration files for different environments
    ├── domain/                     # LAYER 1: Enterprise Business Rules
    ├── service_layer/              # LAYER 2: Application / Use Case Logic
    ├── adapters/                   # LAYER 3: Infrastructure / Plugins
    ├── scripts/                    # Utility scripts / DevOps tasks
    ├── tests/                      # Testing suite
    └── docs/                       # Documentation
```

### Key Directories

- **`config/`**: Contains environment-specific configurations (e.g., development, production, testing).
- **`domain/`**: Implements core business logic, including entities, domain events, and exceptions.
- **`service_layer/`**: Contains application logic, such as use case handlers and message buses.
- **`adapters/`**: Handles infrastructure concerns, including repositories, entry points (e.g., Flask API), and external integrations.
- **`scripts/`**: Utility scripts for tasks like database migrations, seeding data, and monitoring.
- **`tests/`**: Unit and integration tests to ensure the reliability of the system.
- **`docs/`**: Documentation files, including architecture diagrams and workflow descriptions.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/) for dependency management
- A running PostgreSQL database (if using the production configuration)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/elainehello/inventory-allocation.git
   cd allocation-service
   ```

2. Install dependencies:

   ```bash
   poetry install
   ```

3. Set up environment variables:

   Create a `.env` file in the root directory and configure the necessary environment variables (e.g., database URL, secrets).

### Running the Application

1. Start the Flask application:

   ```bash
   poetry run flask run
   ```

2. Access the API at `http://127.0.0.1:5000`.

### Running Tests

Run the test suite using the following command:

```bash
poetry run pytest
```

## Documentation

- **Architecture**: See [docs/architecture.md](src/allocation/docs/architecture.md) for an overview of the system design.
- **Workflows**: See [docs/workflows.md](src/allocation/docs/workflows.md) for domain workflows and event flows.
- **Database Schema**: Refer to the ERD diagram at [docs/erd.png](src/allocation/docs/erd.png).

## Contributing

1. Fork the repository.
2. Create a feature branch.
3. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.