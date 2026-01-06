# ML Spam Classifier - Notebooks

Notebooks de análise exploratória e treinamento de modelos para classificação de spam.

## Dataset

**Nome:** Email Spam Classification Dataset  
**Fonte:** Kaggle (purusinghvi, 2023)  
**Total:** 83,448 emails  
**Distribuição:** 52.62% spam, 47.38% ham  
**Localização:** `data/emails.csv`

## Instalação

Execute na raiz do projeto:

```bash
make install
```

Isso irá:
1. Criar o ambiente virtual em `notebooks/venv`
2. Instalar todas as dependências
3. Instalar o kernel Jupyter "ML Spam Classifier"

## Ambiente Virtual

### Ativar ambiente manualmente

```bash
cd notebooks
source venv/bin/activate
```

## Jupyter Kernel

**Nome:** ML Spam Classifier  
**Kernel instalado em:** `~/.local/share/jupyter/kernels/ml-spam-classifier`

### Como usar

1. Execute `make install` na raiz do projeto (instala kernel automaticamente)
2. Abra o Jupyter Notebook ou VSCode
3. Selecione o kernel "ML Spam Classifier"
4. Execute os notebooks na ordem:
   - `01_exploratory_analysis.ipynb` - Análise exploratória e preparação dos dados
   - `02_model_selection.ipynb` - Seleção do melhor modelo
   - `03_hyperparameter_tuning.ipynb` - Otimização de hiperparâmetros
   - `04_pipeline.ipynb` - Pipeline final para produção

### Remover kernel (se necessário)

```bash
jupyter kernelspec uninstall ml-spam-classifier
```

## Notebooks

### 01 - Exploratory Data Analysis
- Carregamento dos dados
- Análise de distribuição
- Análise de texto
- Palavras mais comuns
- Visualizações

### 02 - Model Selection
- Carregamento dos dados processados
- Treinamento de múltiplos modelos (Naive Bayes, Logistic Regression, SVM, Random Forest, XGBoost)
- Comparação de métricas (Accuracy, Precision, Recall, F1-Score)
- Seleção do melhor modelo
- Visualizações comparativas

### 03 - Hyperparameter Tuning
- Carregamento do melhor modelo do notebook 02
- Otimização de hiperparâmetros com RandomizedSearchCV
- Comparação baseline vs otimizado
- Export do modelo otimizado

### 04 - Pipeline Final
- Treinamento do modelo final com 100% dos dados
- Validação com cross-validation
- Export de artefatos para produção (modelo, vetorizador, metadados)

## Testes com Datasets Externos

Após treinar o modelo, é possível testá-lo usando datasets externos que não foram usados no treinamento. Isso ajuda a validar a capacidade de generalização do modelo.

Veja a pasta `teste/` para scripts e documentação sobre como:
- Baixar datasets externos (Kaggle SMS Spam Collection)
- Testar o modelo via API
- Gerar relatório de performance

```bash
cd notebooks/teste
python baixar_datasets.py
python testar_modelo_api.py
```

## Dependências Principais

- pandas 2.2.3
- scikit-learn 1.5.2
- nltk 3.9.1
- matplotlib 3.9.2
- seaborn 0.13.2
- wordcloud 1.9.3
- requests 2.31.0


