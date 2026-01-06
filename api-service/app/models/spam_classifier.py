"""
Modelo de classificação de spam em emails.

Carrega e gerencia modelo treinado para identificar spam.
"""

from pathlib import Path
from typing import Any, Dict

import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.calibration import CalibratedClassifierCV


class SpamClassifier:
    """Classificador de spam usando modelo treinado."""

    def __init__(self, models_dir: str = "models"):
        """Inicializa o classificador.

        Args:
            models_dir: Caminho para pasta com modelos exportados
        """
        self.models_dir = Path(models_dir)
        self.model = None
        self.vectorizer = None
        self.label_encoder = None
        self.metadata = None
        self.is_loaded = False

    def load(self) -> None:
        """Carrega modelo e artefatos necessários."""
        try:
            model_path = self.models_dir / "best_model_temp.joblib"
            self.model = joblib.load(model_path)

            vectorizer_path = self.models_dir / "tfidf_vectorizer.joblib"
            self.vectorizer = joblib.load(vectorizer_path)

            # Carregar label_encoder se existir (para LinearSVC)
            label_encoder_path = self.models_dir / "label_encoder.joblib"
            if label_encoder_path.exists():
                self.label_encoder = joblib.load(label_encoder_path)

            metadata_path = self.models_dir / "metadata.joblib"
            if metadata_path.exists():
                self.metadata = joblib.load(metadata_path)
            else:
                self.metadata = {}

            self.is_loaded = True

        except Exception as e:
            raise RuntimeError(f"Erro ao carregar modelo: {str(e)}")

    def classify(self, data: Dict[str, Any], threshold: float = 0.5) -> Dict[str, Any]:
        """Classifica email como spam ou ham.

        Args:
            data: Dicionário com dados do email (campo 'message')
            threshold: Threshold de probabilidade para classificar como spam (padrão: 0.5)
                       Valores mais altos (0.7-0.8) reduzem falsos positivos

        Returns:
            Dicionário com resultado da classificação
        """
        if not self.is_loaded:
            raise RuntimeError("Modelo não carregado. Execute .load() primeiro.")

        message = data.get("message", "")
        if not message:
            raise ValueError("Mensagem não pode estar vazia")

        message_vectorized = self.vectorizer.transform([message])
        
        # Verificar se o modelo tem predict_proba
        model_type = type(self.model).__name__
        
        if hasattr(self.model, 'predict_proba'):
            # Modelo tem predict_proba (MultinomialNB, LogisticRegression, etc)
            probabilities = self.model.predict_proba(message_vectorized)[0]
            classes = self.model.classes_
            spam_idx = list(classes).index('spam') if 'spam' in classes else 1
            ham_idx = list(classes).index('ham') if 'ham' in classes else 0
        elif 'LinearSVC' in model_type:
            # LinearSVC não tem predict_proba, usar decision_function
            # Converter decision scores para probabilidades usando sigmoid
            decision = self.model.decision_function(message_vectorized)[0]
            # Sigmoid: P(spam) = 1 / (1 + exp(-decision))
            # Se decision > 0, mais provável spam; se < 0, mais provável ham
            probability_spam = 1 / (1 + np.exp(-decision))
            probability_ham = 1 - probability_spam
            
            # Normalizar para garantir soma = 1
            total = probability_spam + probability_ham
            probability_spam = probability_spam / total
            probability_ham = probability_ham / total
            
            probabilities = np.array([probability_ham, probability_spam])
            spam_idx = 1
            ham_idx = 0
        else:
            # Fallback: tentar predict_proba ou usar decision_function
            if hasattr(self.model, 'predict_proba'):
                probabilities = self.model.predict_proba(message_vectorized)[0]
            else:
                decision = self.model.decision_function(message_vectorized)[0]
                probability_spam = 1 / (1 + np.exp(-decision))
                probability_ham = 1 - probability_spam
                probabilities = np.array([probability_ham, probability_spam])
            
            classes = self.model.classes_ if hasattr(self.model, 'classes_') else ['ham', 'spam']
            spam_idx = list(classes).index('spam') if 'spam' in classes else 1
            ham_idx = list(classes).index('ham') if 'ham' in classes else 0

        probability_spam = float(probabilities[spam_idx])
        probability_ham = float(probabilities[ham_idx])
        
        is_spam = probability_spam >= threshold
        confidence = probability_spam if is_spam else probability_ham

        return {
            "prediction": "spam" if is_spam else "ham",
            "is_spam": is_spam,
            "confidence": round(confidence, 4),
            "probability_spam": round(probability_spam, 4),
            "probability_ham": round(probability_ham, 4),
            "model_info": {
                "type": self.metadata.get("model_type", "LinearSVC"),
                "vectorizer": "TfidfVectorizer",
            },
        }

    def get_model_info(self) -> Dict[str, Any]:
        """Retorna informações sobre o modelo carregado."""
        if not self.is_loaded:
            return {"loaded": False}

        return {
            "loaded": True,
            "model_type": self.metadata.get("model_type", "LinearSVC"),
            "vectorizer_type": "TfidfVectorizer",
            "training_samples": self.metadata.get("training_samples"),
            "accuracy": self.metadata.get("optimization_accuracy"),
            "precision": self.metadata.get("optimization_precision"),
            "recall": self.metadata.get("optimization_recall"),
            "f1_score": self.metadata.get("optimization_f1") or self.metadata.get("cv_f1_mean"),
            "trained_date": self.metadata.get("trained_date"),
            "cv_f1_mean": self.metadata.get("cv_f1_mean"),
            "cv_f1_std": self.metadata.get("cv_f1_std"),
        }





