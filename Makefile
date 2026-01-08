.PHONY: help install deploy-models dev dev-full test build up up-full down logs clean

help:
	@echo "ML Spam Classifier - Makefile"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install notebook dependencies (venv) + Jupyter kernel"
	@echo "  make deploy-models  - Copy trained models from notebooks to API"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Start API only (hot reload)"
	@echo "  make dev-full       - Start API + Frontend (full stack)"
	@echo "  make test           - Run tests (multi-stage build)"
	@echo "  make logs           - Show API logs"
	@echo ""
	@echo "Production:"
	@echo "  make build          - Build all images (API + Frontend)"
	@echo "  make up             - Start API only"
	@echo "  make up-full        - Start API + Frontend"
	@echo "  make down           - Stop all containers"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean          - Clean cache and temporary files"

install:
	@echo "Installing notebook dependencies (venv only)..."
	@if [ ! -f ./configs/.env ]; then \
		echo "Criando configs/.env a partir do template..."; \
		cp ./configs/.env.example ./configs/.env; \
	fi
	@echo ""
	@echo "1. Criando venv e instalando dependências..."
	@cd notebooks && python3 -m venv venv
	@cd notebooks && . venv/bin/activate && pip install -r requirements.txt
	@echo ""
	@echo "2. Instalando kernel Jupyter..."
	@cd notebooks && . venv/bin/activate && python -m ipykernel install --user --name=ml-spam-classifier --display-name="ML Spam Classifier"
	@echo ""
	@echo "✓ Notebook environment ready!"
	@echo "✓ Jupyter kernel 'ML Spam Classifier' instalado!"
	@echo ""
	@echo "NOTE: API runs ONLY in Docker. Use 'make dev' to start."
	@echo "NOTE: Selecione o kernel 'ML Spam Classifier' nos notebooks Jupyter."

deploy-models:
	@echo "Deploying ML models to API..."
	python scripts/deploy_models.py
	@echo "✓ Models deployed!"

dev:
	@echo "Starting API in DEVELOPMENT mode (hot reload)..."
	@echo ""
	@if [ ! -f ./configs/.env ]; then \
		echo "  configs/.env não encontrado. Copiando de .env.example..."; \
		cp ./configs/.env.example ./configs/.env; \
	fi
	@docker compose --env-file ./configs/.env --profile api down 2>/dev/null || true
	@DEV_VOLUME=rw API_COMMAND=dev LOG_LEVEL=debug docker compose --env-file ./configs/.env --profile api up --build
	@echo ""
	@echo "API stopped."

dev-full:
	@echo "Starting FULL STACK in DEVELOPMENT mode..."
	@echo ""
	@if [ ! -f ./configs/.env ]; then \
		echo "  configs/.env não encontrado. Copiando de .env.example..."; \
		cp ./configs/.env.example ./configs/.env; \
	fi
	@docker compose --env-file ./configs/.env --profile full down 2>/dev/null || true
	@DEV_VOLUME=rw API_COMMAND=dev LOG_LEVEL=debug docker compose --env-file ./configs/.env --profile full up --build
	@echo ""
	@echo "Services stopped."

test:
	@echo "Running tests..."
	@echo ""
	@docker compose --env-file ./configs/.env --profile test down 2>/dev/null || true
	@docker compose --env-file ./configs/.env --profile test build --no-cache test
	@docker compose --env-file ./configs/.env --profile test up --abort-on-container-exit test
	@docker compose --env-file ./configs/.env --profile test down
	@echo ""
	@echo "✓ Tests complete! Coverage: api-service/htmlcov/index.html"

build:
	@echo "Building PRODUCTION images..."
	@docker compose --env-file ./configs/.env build --no-cache api frontend
	@echo "✓ Production images built!"

up:
	@echo "Starting PRODUCTION API..."
	@if [ ! -f ./configs/.env ]; then \
		echo "  configs/.env não encontrado. Copiando de .env.example..."; \
		cp ./configs/.env.example ./configs/.env; \
	fi
	@docker compose --env-file ./configs/.env --profile api down 2>/dev/null || true
	@docker compose --env-file ./configs/.env --profile api up -d
	@PORT=$$(grep '^PORT=' ./configs/.env | cut -d'=' -f2 || echo 8000); \
	echo ""; \
	echo "✓ API running!"; \
	echo "  URL: http://localhost:$$PORT"; \
	echo "  Docs: http://localhost:$$PORT/docs"; \
	echo ""; \
	echo "View logs: make logs"

up-full:
	@echo "Starting FULL STACK in PRODUCTION..."
	@if [ ! -f ./configs/.env ]; then \
		echo "  configs/.env não encontrado. Copiando de .env.example..."; \
		cp ./configs/.env.example ./configs/.env; \
	fi
	@docker compose --env-file ./configs/.env --profile full down 2>/dev/null || true
	@docker compose --env-file ./configs/.env --profile full up -d
	@PORT=$$(grep '^PORT=' ./configs/.env | cut -d'=' -f2 || echo 8000); \
	echo ""; \
	echo "✓ Full stack running!"; \
	echo "  Frontend: http://localhost:3000"; \
	echo "  API: http://localhost:$$PORT"; \
	echo "  Docs: http://localhost:$$PORT/docs"; \
	echo ""; \
	echo "View logs: make logs"

down:
	@echo "Stopping all containers..."
	@docker compose --env-file ./configs/.env --profile api down 2>/dev/null || true
	@docker compose --env-file ./configs/.env --profile frontend down 2>/dev/null || true
	@docker compose --env-file ./configs/.env --profile full down 2>/dev/null || true
	@docker compose --env-file ./configs/.env --profile test down 2>/dev/null || true
	@echo "✓ Stopped!"

logs:
	@echo "Logs (Ctrl+C to exit):"
	@echo ""
	@docker compose --env-file ./configs/.env logs -f api frontend 2>/dev/null || docker compose --env-file ./configs/.env --profile api logs -f api

clean:
	@echo "Cleaning cache and temporary files..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	@echo "✓ Cleanup complete!"

