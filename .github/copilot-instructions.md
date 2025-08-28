# Copilot Instructions for AI Coding Agents

## Project Overview
This repository implements a Smart Home Energy Monitoring system with Conversational AI. The architecture consists of three main backend services (Authentication, Telemetry, Conversational AI), a PostgreSQL database, and a Next.js frontend. All components are containerized with Docker and orchestrated via `docker-compose` for local development.

## Key Components
- **backend/**: Contains all backend services (Auth, Telemetry, Conversational AI). Each service should be independently runnable and expose a RESTful API (documented with Swagger/OpenAPI).
- **frontend/**: Next.js single-page application for user login, device dashboards, and optional conversational interface.
- **docker-compose.yml**: Orchestrates all services and the database for local development.

## Developer Workflows
- **Start all services locally:**
  ```
  docker-compose up --build
  ```
- **Run backend tests:**
  - Use `pytest` inside the relevant backend service container.
- **API Documentation:**
  - Each backend service should expose Swagger/OpenAPI docs at `/docs` or similar endpoint.
- **Database:**
  - Uses PostgreSQL, seeded with demo users/devices.
  - Prisma ORM is used for database access.

## Project Conventions
- Each backend service is a separate FastAPI app.
- All inter-service communication is via REST APIs (no direct DB access across services).
- Use JWT for authentication; Auth service issues tokens.
- All code should be containerized and runnable via Docker Compose.
- Use environment variables for secrets/configuration (see `docker-compose.yml`).
- Follow modular implementation principles (e.g., separate concerns, single responsibility).
- Write unit tests for all new features and bug fixes.
- Document all APIs using OpenAPI/Swagger.
- Use consistent coding styles and best practices (PEP 8 for Python, etc.).
- Include error handling and input validation.
- Optimize for performance and scalability.

## Patterns & Examples
- **Telemetry data**: POST to Telemetry API with `{timestamp, deviceId, energy usage}`.
- **Conversational queries**: POST user questions to Conversational AI API, receive structured summaries or time-series data.
- **Frontend**: Authenticates via Auth API, fetches device/telemetry data via REST, displays charts and conversational responses.

## References
- See `README.md` in the root for architecture and tech stack.
- See `docker-compose.yml` for service definitions and environment variables.

---
If you are unsure about a workflow or convention, prefer patterns shown in the root `README.md` and ensure all services remain independently deployable and API-driven.
