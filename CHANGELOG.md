# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2026-01-06

### Added
- Complete ML pipeline with 4 Jupyter notebooks (EDA, model selection, hyperparameter tuning, final pipeline)
- SVM (LinearSVC) model with TF-IDF vectorization (5000 features)
- FastAPI backend with MVC architecture
- React frontend with TypeScript and TailwindCSS
- Docker multi-stage builds for API and Frontend
- Unit tests with coverage reporting
- Postman collection with examples
- Architecture diagrams and documentation
- Environment variables configuration in `configs/.env`
- Jupyter kernel automatic installation via Makefile
- Script `deploy_models.py` for model deployment
- Comprehensive test suite (routers, controllers, models)
- Test fixtures and mocks
- Frontend component with probability percentages display

### Changed
- Unified docker-compose files into single `docker-compose.yml`
- Environment variables moved to `configs/.env`
- Makefile updated to use `--env-file ./configs/.env`
- Model migrated from Multinomial Naive Bayes to SVM (LinearSVC)
- Notebooks simplified to use LinearSVC directly (removed conditional checks)

### Fixed
- Schema consistency between frontend and backend
- Added `is_spam` field to frontend TypeScript types
- Removed incompatible `pytest-asyncio` dependency
- Test structure and coverage configuration
- Model metadata loading in API
- Removed emojis from Python code
