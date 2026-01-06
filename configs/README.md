# Configurações

Pasta com arquivos de configuração.

## Arquivos

- `.env.example` - Template de variáveis (versionado)
- `.env` - Variáveis reais (não versionado)

## Primeira vez

```bash
cp configs/.env.example configs/.env
```

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
```

**Nota:** O `.env` não é commitado. Use `.env.example` como base.

