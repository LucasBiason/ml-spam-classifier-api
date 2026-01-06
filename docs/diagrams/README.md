# Diagramas de Arquitetura

Este diretório contém os arquivos fonte dos diagramas Mermaid usados na documentação.

## Arquivos

### architecture-beta.mmd
Diagrama simplificado de arquitetura (usado no README):
- Layout moderno com architecture-beta
- Grupos: Client, Frontend, Backend, ML, Data
- Fluxo visual limpo
- **Renderizado em:** `docs/screenshots/app-beta.png`

### architecture-flow.mmd
Diagrama completo tradicional (flowchart):
- Client Layer (User, Browser)
- Frontend Layer (React, Nginx)
- Backend Layer (FastAPI, Routers, Controllers)
- ML Layer (LinearSVC, TfidfVectorizer)
- Data Pipeline (Notebooks, Dataset)
- **Renderizado em:** `docs/screenshots/app-architecture.png`

### request-sequence.mmd
Diagrama de sequência mostrando o fluxo de requisição:
- User → Frontend → API → ML
- Response flow completo
- Processamento de texto

**Renderizado em:** `docs/screenshots/sequence-diagram.png` (opcional)

## Como Gerar Imagens

### Opção 1: VS Code (Mermaid Preview)
1. Instalar extensão "Mermaid Preview"
2. Abrir arquivo .mmd
3. Ctrl+Shift+P → "Mermaid: Preview"
4. Screenshot do preview

### Opção 2: Online (Mermaid Live Editor)
1. Acessar: https://mermaid.live/
2. Copiar código do arquivo .mmd
3. Colar no editor
4. Download PNG

### Opção 3: CLI (mmdc)
```bash
npm install -g @mermaid-js/mermaid-cli
mmdc -i architecture-flow.mmd -o ../screenshots/app-flow.png
```

## Cores Usadas

- **Frontend**: #61DAFB (React Blue)
- **Backend**: #009688 (Teal)
- **ML Layer**: #FF6F00 (Orange)
- **Data**: #4CAF50 (Green)

