# Introduction
This project is a comprehensive solution for the Smart Home Energy Monitoring system with Conversational AI.
The Smart Home Energy Monitoring system comprises three primary backend services: an Authentication Service, a Telemetry Service, and a Conversational AI Service. These services interact with a PostgreSQL database for data persistence and are containerized using Docker, orchestrated via docker-compose for local development and deployment. A single-page application (SPA) serves as the frontend, providing user interaction, data visualization, and an optional conversational interface.

The goal is to build a functional prototype that allows users to monitor and understand their energy consumption through dashboards and natural-language questions.

# Core Scope

## Backend Services

- Auth Service: Handles user registration, login, JWT issuance, and role management.

- Telemetry Service: Accepts and stores device telemetry (timestamp, deviceId, energy usage).

- Conversational AI Service: Receives user questions, interprets intent, and returns structured summaries and/or time-series data. Can use rules-based parser, deterministic logic, or integrate with a public LLM.

- APIs: Expose RESTful APIs for each service with OpenAPI/Swagger or Postman documentation.

## Frontend 

- Login/Register flow.

- List of devices.

- Device dashboard with one line or bar chart showing recent energy usage (e.g., last 7 days).

- Optional: Text input to ask natural-language questions and view structured responses.

## Data Persistence

- Use PostgreSQL (or similar) to store:

- Users and their roles.

- Devices linked to users.

- Timestamped telemetry data.

- Seed a few users and devices for demonstration.

## DevOps & Deploy

- Use Docker to containerize all services and PostgreSQL.

- Provide a docker-compose.yml to run the entire system locally.

- Each service should run independently and expose its own API.


# Tech Stack




