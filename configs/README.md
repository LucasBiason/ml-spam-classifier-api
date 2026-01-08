# Configurações

Pasta com arquivos de configuração.

## Arquivos

- `.env.example` - Template de variáveis (versionado)
- `.env` - Variáveis reais (não versionado)

## Primeira vez

```bash
cp configs/.env.example configs/.env
```

## Variáveis de Ambiente

Todas as variáveis são carregadas do arquivo `configs/.env`. O `docker-compose.yml` usa apenas `env_file` e não define variáveis diretamente.

### Variáveis Disponíveis

**Python:**
- `PYTHONPATH=/app` - Caminho Python para imports
- `PYTHONUNBUFFERED=1` - Output não bufferizado (logs em tempo real)

**API:**
- `API_COMMAND=runserver` - Comando da API (runserver/dev)
- `PORT=8000` - Porta da API
- `WORKERS=4` - Número de workers (produção)
- `LOG_LEVEL=info` - Nível de log (info/debug/warning/error)

**Development:**
- `DEV_VOLUME=ro` - Permissão do volume (ro=read-only, rw=read-write)

**Frontend:**
- `VITE_API_URL=http://localhost:8000` - URL da API para o frontend

**Network:**
- `NETWORK_NAME=ml-spam-network` - Nome da rede Docker

## Desenvolvimento

O `.env` padrão funciona. Para hot reload, use `make dev` que ajusta automaticamente.

Ou edite manualmente:

```bash
DEV_VOLUME=rw
API_COMMAND=dev
LOG_LEVEL=debug
```

## Produção (Hostinger VPS)

Edite `configs/.env`:

```bash
PORT=8002
NETWORK_NAME=portfolio-net
VITE_API_URL=
LOG_LEVEL=info
WORKERS=4
```

**Nota:** O `.env` não é commitado. Use `.env.example` como base.

