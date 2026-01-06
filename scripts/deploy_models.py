"""
Script para deploy de modelos.

Copia modelos treinados dos notebooks para api-service.
Apenas modelos finais de produção.
"""

import shutil
from pathlib import Path


def deploy_models():
    """Copia modelos finais dos notebooks para api-service."""
    project_root = Path(__file__).parent.parent

    source_dir = project_root / "notebooks" / "artifacts"
    target_dir = project_root / "api-service" / "models"

    target_dir.mkdir(exist_ok=True)

    models_to_copy = [
        "best_model_temp.joblib",
        "tfidf_vectorizer.joblib",
        "label_encoder.joblib",  # Necessário para LinearSVC
        "metadata.joblib",  # Metadados do modelo
    ]

    print("=" * 80)
    print("DEPLOY DE MODELOS ML SPAM CLASSIFIER")
    print("=" * 80)
    print(f"\nOrigem: {source_dir.absolute()}")
    print(f"Destino: {target_dir.absolute()}")
    print(f"\nModelos para deploy: {len(models_to_copy)}")

    copied_count = 0
    not_found_count = 0

    for model_file in models_to_copy:
        source_path = source_dir / model_file
        target_path = target_dir / model_file

        if not source_path.exists():
            print(f"\n[ERRO] NÃO ENCONTRADO: {model_file}")
            not_found_count += 1
            continue

        shutil.copy2(source_path, target_path)
        size_mb = target_path.stat().st_size / (1024 * 1024)

        print(f"\n[OK] COPIADO: {model_file}")
        print(f"  Tamanho: {size_mb:.2f} MB")
        copied_count += 1

    print("\n" + "=" * 80)
    if copied_count == len(models_to_copy):
        print("DEPLOY CONCLUÍDO!")
    else:
        print(f"DEPLOY PARCIAL: {copied_count}/{len(models_to_copy)} modelos copiados")
        if not_found_count > 0:
            print(f"[AVISO] {not_found_count} modelo(s) não encontrado(s). Treine os modelos primeiro.")
    print("=" * 80)
    print("\nModelos prontos em: api-service/models/")


if __name__ == "__main__":
    deploy_models()
