#!/usr/bin/env bash
set -euo pipefail

check_models() {
  if [ ! -f "./models/best_model_temp.joblib" ] || [ ! -f "./models/tfidf_vectorizer.joblib" ]; then
    echo "WARNING: Model files not found in ./models/" >&2
    return 1
  fi
  return 0
}

case "${1:-runserver}" in
  test)
    pytest -c tests/pytest.ini
    ;;

  dev)
    check_models || true
    PORT=${PORT:-8000}
    LOG_LEVEL=${LOG_LEVEL:-debug}
    exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$PORT" \
      --reload \
      --log-level "$LOG_LEVEL"
    ;;

  runserver)
    check_models || exit 1
    PORT=${PORT:-8000}
    WORKERS=${WORKERS:-4}
    LOG_LEVEL=${LOG_LEVEL:-info}
    exec uvicorn app.main:app \
      --host 0.0.0.0 \
      --port "$PORT" \
      --workers "$WORKERS" \
      --log-level "$LOG_LEVEL"
    ;;
esac

