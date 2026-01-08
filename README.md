# ML Spam Classifier - Email Classification Service

[![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen.svg)](api-service/htmlcov/index.html)
[![Python](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev/)
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)

API para classificação de emails em spam ou ham usando SVM (LinearSVC) com TF-IDF. Inclui backend FastAPI e frontend React.

## Preview

![Spam Classification Result](docs/screenshots/spam-classification.png)

*Interface completa mostrando formulário de entrada de email e resultado da classificação em tempo real. O sistema classifica corretamente emails como SPAM (vermelho) ou HAM (verde) com percentuais de confiança.*

## Arquitetura

*Diagrama simplificado da arquitetura mostrando fluxo entre Client, Frontend, Backend e ML.*

### Fluxo de Requisição

1. **User** digita mensagem de email no navegador
2. **React** valida e envia POST para `/predict`
3. **FastAPI** recebe via Router e delega para Controller
4. **Controller** chama `SpamClassifier.predict()`
5. **SVM (LinearSVC)** processa texto com TfidfVectorizer
6. **Model** retorna classificação (spam/ham) com confiança
7. **API** retorna JSON com resultado
8. **React** renderiza resultado na interface

### Request/Response Example

**Frontend → Backend:**
```json
POST /predict
Content-Type: application/json

{
  "message": "Win a free iPhone now! Click here!",
  "threshold": 0.5
}
```

**Nota:** O parâmetro `threshold` é opcional (padrão: 0.5). Valores mais altos (0.7-0.8) reduzem falsos positivos, mas podem aumentar falsos negativos.

**Backend → Frontend:**
```json
{
  "prediction": "spam",
  "is_spam": true,
  "confidence": 0.985,
  "probability_spam": 0.985,
  "probability_ham": 0.015,
  "model_info": {
    "type": "LinearSVC",
    "vectorizer": "TfidfVectorizer"
  }
}
```

## Características

- **Machine Learning**: SVC (Support Vector Classifier) com TF-IDF (5000 features)
- **Frontend**: React com TailwindCSS e TypeScript
- **API**: FastAPI com Swagger/ReDoc
- **Testes**: Cobertura de código configurada
- **Docker**: Stack completo containerizado
- **Performance**: Classificação em tempo real com scores de confiança

## Tecnologias

### Frontend
- React 18 + TypeScript
- Vite (Build tool)
- TailwindCSS (Styling)
- Axios (HTTP client)
- Lucide React (Icons)
- Nginx (Production server)

### Backend
- Python 3.13
- FastAPI (API REST)
- scikit-learn (LinearSVC, TfidfVectorizer)
- pandas, numpy (Processamento de dados)
- joblib (Serialização de modelos)
- pytest, pytest-cov (Testes e cobertura)

### DevOps
- Docker & Docker Compose (Multi-stage builds)
- Makefile (Automação)

## Estrutura do Projeto

```
ml-spam-classifier-api/
├── notebooks/                    # Jupyter notebooks (venv)
│   ├── 01_exploratory_analysis.ipynb
│   ├── 02_model_selection.ipynb
│   ├── 03_hyperparameter_tuning.ipynb
│   ├── 04_pipeline.ipynb
│   └── artifacts/                 # Modelos treinados
│       ├── best_model_temp.joblib
│       ├── tfidf_vectorizer.joblib
│       ├── metadata.joblib
│       └── data_splits.joblib
│
├── api-service/                   # FastAPI (Docker only)
│   ├── app/
│   │   ├── main.py
│   │   ├── models/
│   │   │   └── spam_classifier.py
│   │   ├── controllers/
│   │   ├── routers/
│   │   ├── schemas/
│   │   └── core/
│   ├── tests/                     # Testes unitários
│   ├── models/                     # Modelos em produção
│   ├── Dockerfile                  # Multi-stage (base, test, production)
│   ├── entrypoint.sh               # CLI entrypoint
│   ├── requirements.txt            # Produção
│   └── pytest.ini                  # Configuração de testes
│
├── frontend/                       # React application
│   ├── src/
│   │   ├── components/
│   │   │   ├── EmailForm.tsx
│   │   │   ├── PredictionResult.tsx
│   │   │   ├── Header.tsx
│   │   │   ├── Footer.tsx
│   │   │   ├── APIStatus.tsx
│   │   │   └── OfflineAlert.tsx
│   │   ├── services/
│   │   │   └── api.ts
│   │   ├── types/
│   │   │   └── index.ts
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── Dockerfile                  # Multi-stage (build, production)
│   ├── nginx.conf                  # Nginx config para SPA
│   └── package.json
│
├── scripts/
│   └── deploy_models.py            # Copia modelos para API
│
├── configs/
│   ├── .env.example               # Template de variáveis de ambiente
│   ├── .env                        # Variáveis de ambiente (não versionado)
│   └── README.md                   # Documentação de configuração
│
├── docs/
│   ├── ARCHITECTURE.md             # Documentação técnica
│   ├── SUMMARY.md                  # Resumo do projeto
│   └── ML_Spam_Classifier_API.postman_collection.json
│
├── docker-compose.yml              # Docker Compose unificado
├── Makefile                        # Comandos simplificados
└── README.md
```

## Quick Start

### 1. Pré-requisitos

- Docker & Docker Compose
- Python 3.13+ (apenas para notebooks)
- Git

### 2. Clone o repositório

```bash
git clone https://github.com/LucasBiason/ml-spam-classifier-api.git
cd ml-spam-classifier-api
```

### 3. Configurar variáveis de ambiente

```bash
# Copiar template e ajustar se necessário
cp configs/.env.example configs/.env

# Editar configs/.env para ajustar configurações
# Para produção, ajuste PORT e NETWORK_NAME
```

### 4. Setup (primeira vez)

```bash
# Instalar dependências dos notebooks e criar kernel Jupyter
make install

# Copiar modelos treinados para a API (após treinar os modelos)
make deploy-models
```

### 5. Rodar aplicação completa (Docker)

```bash
# Full stack (API + Frontend)
make dev-full
```

Acesse:
- **Frontend**: http://localhost:3000
- **API**: http://localhost:8000 (ou porta configurada em configs/.env)
- **Docs**: http://localhost:8000/docs

### 6. Rodar testes

```bash
# Testes em Docker (igual ao CI/CD)
make test
```

Relatório de coverage: `api-service/htmlcov/index.html`

## Comandos Disponíveis

### Setup
```bash
make install        # Instalar notebooks (venv)
make deploy-models  # Copiar modelos para API
```

### Development (Docker)
```bash
make dev            # API only (hot reload)
make dev-full       # API + Frontend (full stack)
make test           # Rodar testes
make logs           # Ver logs
make down           # Parar containers
```

### Production (Docker)
```bash
make build          # Build API + Frontend
make up             # Start API only
make up-full        # Start API + Frontend
make down           # Parar tudo
```

### Utilities
```bash
make clean          # Limpar cache
make help           # Ver todos os comandos
```

## Endpoints da API

### Health Check
```bash
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "classifier_ready": true,
  "timestamp": "2024-01-15T10:30:00"
}
```

### Model Information
```bash
GET /api/v1/model/info
```

**Response:**
```json
{
  "loaded": true,
  "model_type": "LinearSVC",
  "vectorizer_type": "TfidfVectorizer",
  "training_samples": 83448,
  "accuracy": 0.985,
  "precision": 0.978,
  "recall": 0.991,
  "f1_score": 0.984
}
```

### Classify Email
```bash
POST /api/v1/predict
```

**Request:**
```json
{
  "message": "Hello, how are you? I wanted to follow up on our meeting.",
  "threshold": 0.5
}
```

**Nota:** O parâmetro `threshold` é opcional (padrão: 0.5). Valores mais altos (0.7-0.8) reduzem falsos positivos, mas podem aumentar falsos negativos.

**Response:**
```json
{
  "prediction": "ham",
  "is_spam": false,
  "confidence": 0.985,
  "probability_spam": 0.015,
  "probability_ham": 0.985,
  "model_info": {
    "type": "LinearSVC",
    "vectorizer": "TfidfVectorizer"
  }
}
```

## Frontend React

### Interface

Interface focada em usabilidade:

- **Layout responsivo**: Grid adaptável (desktop: 2 colunas, mobile: stack)
- **Dark mode**: Suporte automático
- **Real-time feedback**: Loading states e validação
- **API status**: Indicador online/offline no header
- **Error handling**: Mensagens claras de erro

### Componentes

**EmailForm** - Formulário de entrada
- Textarea para mensagem de email
- Validação de tamanho (10-5000 caracteres)
- Contador de caracteres
- Loading spinner durante classificação

**PredictionResult** - Exibição de resultado
- Badge destacado (SPAM/HAM)
- Indicador de confiança
- Informações do modelo
- Cores intuitivas (vermelho para spam, verde para ham)

### Validação de Entrada

- **message**: 10-5000 caracteres (obrigatório)
- Validação client-side antes do envio

## Testes

Testes automatizados com relatório de cobertura:

```bash
# Rodar testes localmente (Docker)
make test

# Ver coverage
open api-service/htmlcov/index.html
```

**Cobertura por módulo:**
- `models/` - Modelo ML
- `controllers/` - Lógica de negócio
- `routers/` - Endpoints
- `schemas/` - Validação Pydantic
- `core/` - Configurações
- `main.py` - Inicialização da aplicação

## Modelo ML

### Treinamento
- **Dataset**: Email Spam Classification (83,448 emails)
- **Modelo**: SVC (Support Vector Classifier) otimizado
- **Vectorizer**: TfidfVectorizer (5000 features)
- **Pipeline**: TF-IDF vectorization + classification

### Limitações e Considerações

- **Domínio de Treinamento:** Modelo treinado para emails (83,448 exemplos)
- **Performance em Emails:** Esperada alta (domínio de treino)
- **Performance em SMS:** Reduzida (22.95% accuracy em teste externo)
- **Recomendação:** Use threshold mais alto (0.7-0.8) para reduzir falsos positivos em produção
- **Mensagens Curtas:** Mensagens com menos de 10 caracteres são rejeitadas pela API

### Performance (Dataset de Treino)
- **Accuracy**: 98.5%
- **Precision (Spam)**: 97.8%
- **Recall (Spam)**: 99.1%
- **F1-Score**: 98.4%
- **Training Time**: 0.3s
- **Prediction Time**: < 10ms
- **Cross-validation**: Validado com 5-fold CV

### Detalhes Técnicos
- Vectorização TF-IDF com 5000 features
- Pré-processamento de texto
- Classificação binária spam/ham
- Probabilidades para ambas classes
- Score de confiança calculado a partir da maior probabilidade

## Desenvolvimento

### Arquitetura Docker-First

**Notebooks**: Rodam em venv local (análise de dados)
```bash
cd notebooks
source venv/bin/activate
jupyter notebook
```

**API**: Roda APENAS em Docker (dev + prod)
```bash
# Development (hot reload)
make dev

# Production
make build
make up
```

### Hot Reload (Development)

O comando `make dev` ajusta automaticamente as variáveis no `configs/.env` para desenvolvimento:
- `DEV_VOLUME=rw` - Permite escrita no volume
- `API_COMMAND=dev` - Modo desenvolvimento com hot reload
- `LOG_LEVEL=debug` - Logs detalhados

Mudanças no código recarregam automaticamente.

**Nota:** Todas as variáveis de ambiente são carregadas do arquivo `configs/.env`. O `docker-compose.yml` não define variáveis diretamente, apenas referencia o arquivo via `env_file`.

## Segurança

- **Non-root user**: Container roda como `appuser` (UID 1000)
- **CORS**: Configurado (ajustar origins em produção)
- **Validação**: Pydantic valida todos os inputs
- **Healthcheck**: Monitoramento automático
- **Secrets**: Todas as variáveis de ambiente em `configs/.env` (não versionado)
- **Centralização**: Todas as configurações via `env_file`, sem variáveis hardcoded no `docker-compose.yml`

## Deploy em Produção

### Configuração para Produção

Edite o arquivo `configs/.env` na VPS. Todas as variáveis são carregadas deste arquivo:

```bash
# Python
PYTHONPATH=/app
PYTHONUNBUFFERED=1

# API Configuration
API_COMMAND=runserver
PORT=8002
WORKERS=4
LOG_LEVEL=info

# Development
DEV_VOLUME=ro

# Frontend
VITE_API_URL=

# Network
NETWORK_NAME=portfolio-net
```

**Nota:** O `docker-compose.yml` usa apenas `env_file` e não define variáveis diretamente. Todas as configurações devem estar no `configs/.env`.

### Deploy

```bash
# Build e start
make build
make up-full
```

### Integração com Portfolio Suite

O projeto se integra com o portfolio-suite via Nginx:
- Frontend: `https://lucasbiason.com/ml-spam-classifier`
- API: `https://lucasbiason.com/ml-spam-classifier-api`

**Nota:** O mesmo `docker-compose.yml` é usado para desenvolvimento e produção. As diferenças são controladas pelo arquivo `configs/.env`.

## Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## Autor

**Lucas Biason**
- GitHub: [@LucasBiason](https://github.com/LucasBiason)
- Portfolio: [lucasbiason.com](https://lucasbiason.com)

