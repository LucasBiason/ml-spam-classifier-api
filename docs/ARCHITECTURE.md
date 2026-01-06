# Arquitetura do Sistema

## Diagrama de Arquitetura

![System Architecture Flow](screenshots/app-architecture.png)

*Diagrama completo mostrando todas as camadas: Client, Frontend, Backend, ML e Data Pipeline.*

> **Fonte Mermaid:** [diagrams/architecture-flow.mmd](diagrams/architecture-flow.mmd)

## Componentes

### 1. Frontend (Port 3000)
- **React 18** com TypeScript
- **TailwindCSS** para styling
- **Axios** para HTTP requests
- **Nginx** para servir produção
- **Hot reload** em desenvolvimento

**Componentes principais:**
- `Header` - Título + API status
- `EmailForm` - Entrada de mensagem de email
- `PredictionResult` - Exibição de resultado (spam/ham)
- `APIStatus` - Indicador online/offline
- `OfflineAlert` - Alerta quando API está offline

### 2. Backend (Port 8000)
- **FastAPI** com Pydantic validation
- **MVC Architecture**:
  - `Routers` - Endpoints (view layer)
  - `Controllers` - Business logic
  - `Schemas` - Data validation
- **Multi-worker** em produção (4 workers)
- **Hot reload** em desenvolvimento

### 3. ML Layer
- **SVM (LinearSVC)** (scikit-learn, otimizado)
- **TfidfVectorizer** - Extração de features de texto (5000 features)
- **Text preprocessing** - Limpeza e normalização
- **Binary classification** - spam/ham
- **Confidence score** - Probabilidade da predição
- **Probability scores** - Probabilidades para spam e ham

### 4. Data Pipeline
- **Notebooks Jupyter** para análise
- **Dataset**: 83,448 emails (Kaggle)
- **Feature engineering** (TfidfVectorizer)
- **Model training** (LinearSVC)
- **Export .joblib** para API

## Request Flow Detalhado

### 1. User Input
```json
{
  "message": "Win a free iPhone now! Click here!"
}
```

### 2. Frontend Validation
- Client-side: Validação de tamanho (10-5000 caracteres)
- Contador de caracteres
- Loading state durante classificação

### 3. API Processing
```python
Router → Controller → SpamClassifier.predict()
```

### 4. ML Inference
```python
1. Load model (LinearSVC)
2. Load vectorizer (TfidfVectorizer)
3. Vectorize text (TF-IDF transformation)
4. Predict (spam/ham)
5. Get prediction probabilities
6. Calculate confidence score (max probability)
7. Return prediction, is_spam, confidence, probabilities
```

### 5. Response
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

## Docker Architecture

### Multi-Stage Builds

**API Dockerfile:**
```
Stage 1 (base):    Install production deps
Stage 2 (test):    Run pytest (coverage >= 90%)
Stage 3 (production): Clean image + entrypoint
```

**Frontend Dockerfile:**
```
Stage 1 (build):   npm ci + npm run build
Stage 2 (production): nginx + static files
```

### Docker Compose Profiles

```yaml
profiles:
  test:     Run tests only
  api:      API only
  frontend: Frontend only
  full:     API + Frontend
```

### Commands

```bash
make dev       # API only (hot reload)
make dev-full  # API + Frontend (hot reload)
make test      # Tests in Docker
make up-full   # Production (API + Frontend)
```

## Security

- **Non-root user** em containers
- **CORS** configurado
- **Input validation** (Pydantic)
- **Security headers** (nginx)
- **Healthchecks** em ambos serviços

## Scalability

- **Horizontal**: Multi-worker FastAPI (4 workers)
- **Vertical**: LinearSVC otimizado
- **Cache**: Nginx static assets (1 year)
- **CDN-ready**: Static build otimizado

## Integration

### Portfolio Suite
- Frontend: `https://lucasbiason.com/ml-spam-classifier`
- API: `https://lucasbiason.com/ml-spam-classifier-api`
- Network: `portfolio-net` (Docker)
- Ports: API `8000`, Frontend `3000`

