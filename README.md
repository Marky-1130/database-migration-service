## FastAPI Migration Orchestrator

A lightweight, explicit approach to managing Alembic migrations across modular FastAPI services sharing a single database.

## Problem

As FastAPI projects grow, teams often split logic into modules or services.

However, Alembic expects a single `Base.metadata`, making it difficult to:
- keep migrations centralized
- avoid tight coupling

This project demonstrates a clean solution.

## Solution

So far, this project assumes that you have all your models on a shared library.
However I will be trying to update this project for setups that each service owns its separate models.

## Sample Project Structure

- app-folder
    - database-migration-service                               - This project
    - sample-service                                           - Your service root folder
    - shared_lib                                               - Shared library for your models
        - models
        - shared-config

## USAGE

This project has been setup with a docker container so you need to include this as a service on
your docker-compose.yml

Sample setup on docker-compose

```
  migration-service:
    build:
      context: ./migration_service
    volumes:
      - ./migration_service:/app
      - ./shared_lib:/app/shared_lib
    depends_on:
      mysql:
        condition: service_healthy

```
