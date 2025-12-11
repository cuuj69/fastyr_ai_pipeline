# Fastyr AI Pipeline - Project Structure

This document provides an overview of the project structure and organization of the Fastyr AI Pipeline library.

## Directory Structure

```
fastyr_ai_pipeline/
├── src/                          # Source code directory
│   └── fastyr/                   # Main package
│       ├── __init__.py
│       ├── api/                  # FastAPI application layer
│       │   ├── controllers/      # REST API controllers
│       │   ├── graphql/          # GraphQL schema and resolvers
│       │   ├── middlewares/      # Request/response middlewares
│       │   ├── dependencies/     # Dependency injection for API
│       │   └── main.py           # FastAPI app entry point
│       ├── core/                 # Core business logic
│       │   ├── contracts/        # DTOs and data contracts
│       │   ├── di/               # Dependency injection container
│       │   ├── exceptions.py     # Custom exceptions
│       │   ├── config.py         # Configuration management
│       │   ├── logging/          # Logging configuration
│       │   └── monitoring/       # Metrics and monitoring
│       ├── domain/               # Domain models and entities
│       │   ├── models/           # SQLAlchemy models
│       │   └── entities/         # Domain entities
│       ├── infrastructure/       # Infrastructure layer
│       │   ├── database/         # Database connection and setup
│       │   └── repositories/     # Data access layer
│       ├── services/             # Business services
│       │   ├── interfaces/       # Service interfaces (ABCs)
│       │   └── providers/        # Provider implementations
│       │       ├── pipeline_service.py    # Main pipeline orchestrator
│       │       ├── deepgram_provider.py   # Deepgram STT provider
│       │       ├── openai_provider.py     # OpenAI LLM provider
│       │       ├── elevenlabs_provider.py # ElevenLabs TTS provider
│       │       └── local_storage_provider.py # Local storage provider
│       └── utils/                # Utility functions
│           └── validators.py
│
├── tests/                        # Test suite
│   ├── unit/                     # Unit tests
│   ├── integration/              # Integration tests
│   ├── e2e/                      # End-to-end tests
│   ├── api/                      # API endpoint tests
│   └── fixtures/                 # Test fixtures and data
│
├── docs/                         # Documentation
│   ├── api/                      # API documentation
│   ├── architecture/             # Architecture documentation
│   └── usage_examples.py         # Usage examples
│
├── alembic/                      # Database migrations
│   └── versions/                 # Migration versions
│
├── .github/                      # GitHub configuration
│   └── workflows/                # CI/CD workflows
│
├── helm/                         # Helm charts for Kubernetes
│   └── fastyr/
│
├── k8s/                          # Kubernetes manifests
│   └── base/
│
├── storage/                      # Runtime storage (gitignored)
│
├── setup.py                      # Package setup configuration
├── pyproject.toml                # Modern Python project config
├── MANIFEST.in                   # Package distribution manifest
├── requirements.txt              # Runtime dependencies
├── LICENSE                       # MIT License
└── README.md                     # Project documentation
```

## Architecture Overview

### Layer Architecture

The project follows a clean architecture pattern with clear separation of concerns:

1. **API Layer** (`api/`): FastAPI application with REST and GraphQL endpoints
2. **Core Layer** (`core/`): Business logic, contracts, and configuration
3. **Domain Layer** (`domain/`): Domain models and entities
4. **Infrastructure Layer** (`infrastructure/`): Database, repositories, external integrations
5. **Services Layer** (`services/`): Provider interfaces and implementations

### Provider Pattern

The library uses a provider pattern for flexibility:

- **Interfaces** (`services/interfaces/`): Abstract base classes defining contracts
  - `STTProvider`: Speech-to-Text interface
  - `LLMProvider`: Language Model interface
  - `TTSProvider`: Text-to-Speech interface
  - `StorageProvider`: Storage interface

- **Implementations** (`services/providers/`): Concrete provider implementations
  - Deepgram (STT)
  - OpenAI (LLM)
  - ElevenLabs (TTS)
  - LocalStorage (Storage)

### Pipeline Service

The `PipelineService` (`services/providers/pipeline_service.py`) orchestrates the complete pipeline:
1. Transcribe audio (STT)
2. Process with LLM
3. Synthesize audio (TTS)
4. Store result

## Key Features

### Design Patterns

- **Dependency Injection**: Using `dependency-injector` for IoC
- **Repository Pattern**: Abstract data access layer
- **Provider Pattern**: Pluggable service providers
- **Strategy Pattern**: Interchangeable providers via interfaces

### Technology Stack

- **Framework**: FastAPI for REST/GraphQL API
- **ORM**: SQLAlchemy with async support
- **Migrations**: Alembic
- **GraphQL**: Strawberry
- **Logging**: Structlog
- **Monitoring**: Sentry, Prometheus
- **Testing**: Pytest with async support

## Package Distribution

### Build Configuration

- `setup.py`: Package metadata and dependencies
- `pyproject.toml`: Modern Python project configuration (pytest, coverage)
- `MANIFEST.in`: Files to include in distribution

### Installation

```bash
pip install fastyr-ai-pipeline
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Testing Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **E2E Tests**: Test complete pipeline flows
- **API Tests**: Test HTTP endpoints

## Deployment

The project includes deployment configurations:
- `Dockerfile`: Container image definition
- `helm/`: Helm charts for Kubernetes
- `k8s/`: Kubernetes manifests

Note: These are optional and demonstrate deployment capabilities. The core library can be used independently.

## File Organization Guidelines

- **Source code**: All library code in `src/fastyr/`
- **Tests**: Mirror source structure in `tests/`
- **Documentation**: User-facing docs in `docs/`
- **Configuration**: Root-level config files
- **Build artifacts**: Excluded via `.gitignore`

## Versioning

Current version: `0.1.0` (as defined in `setup.py`)

## License

MIT License - see LICENSE file for details

