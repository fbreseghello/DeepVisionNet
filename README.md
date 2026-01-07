Deep Learning para classificação de dígitos manuscritos usando Redes Neurais Convolucionais (CNN) no dataset MNIST.

## Sobre o Projeto

DeepVisionNet é uma implementação moderna e profissional de classificação de dígitos manuscritos utilizando TensorFlow/Keras. O projeto inclui:

- Arquitetura CNN otimizada com BatchNormalization e Dropout
- Sistema de logging completo para rastreamento de experimentos
- Callbacks avançados (EarlyStopping, ModelCheckpoint, ReduceLROnPlateau)
- Visualizações automáticas de métricas de treinamento
- Argumentos de linha de comando para configuração flexível
- Código orientado a objetos e modular
- Tratamento robusto de erros

## Arquitetura do Modelo

```
Input (28x28x1)
    ↓
Conv2D (32 filters, 3x3) + ReLU + BatchNorm
    ↓
MaxPooling2D (2x2)
    ↓
Conv2D (64 filters, 3x3) + ReLU + BatchNorm
    ↓
MaxPooling2D (2x2)
    ↓
Flatten
    ↓
Dense (128 units) + ReLU
    ↓
Dropout (0.5)
    ↓
Dense (10 units) + Softmax
```

**Parâmetros totais**: ~200K parâmetros treináveis

## Resultados Esperados

- **Acurácia de Teste**: ~99.0-99.5%
- **Loss de Teste**: ~0.03-0.05
- **Tempo de Treinamento**: ~2-5 minutos (CPU) / ~30-60s (GPU)

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/DeepVisionNet.git
cd DeepVisionNet
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Uso

### Treinamento Básico

Execute o script com as configurações padrão:

```bash
python DeepVisionNet.py
```

### Treinamento Personalizado

Configure hiperparâmetros via argumentos de linha de comando:

```bash
python DeepVisionNet.py --epochs 30 --batch-size 256 --learning-rate 0.0005 --output-dir custom_results
```

### Argumentos Disponíveis

| Argumento | Tipo | Padrão | Descrição |
|-----------|------|---------|-----------|
| `--epochs` | int | 20 | Número de épocas de treinamento |
| `--batch-size` | int | 128 | Tamanho do batch |
| `--learning-rate` | float | 0.001 | Taxa de aprendizado |
| `--output-dir` | str | results | Diretório para salvar resultados |

## Estrutura de Saída

Após o treinamento, os seguintes arquivos serão gerados no diretório `results/`:

```
results/
├── model_best_YYYYMMDD_HHMMSS.keras    # Melhor modelo durante treinamento
├── model_final.keras                    # Modelo final
├── model_summary.txt                    # Resumo da arquitetura
├── training_history.png                 # Gráficos de loss e accuracy
├── training_log_YYYYMMDD_HHMMSS.csv    # Log CSV do treinamento
└── training.log                         # Log completo de execução
```

## Features Avançadas

### Callbacks Implementados

1. **ModelCheckpoint**: Salva o melhor modelo baseado na validação
2. **EarlyStopping**: Interrompe treinamento se não houver melhoria
3. **ReduceLROnPlateau**: Reduz learning rate quando métrica estagna
4. **CSVLogger**: Registra métricas em arquivo CSV

### Logging

Sistema de logging em dois níveis:
- Console: Informações principais do progresso
- Arquivo: Log detalhado com timestamps

### Visualizações

Gráficos automáticos de:
- Acurácia (treino vs validação)
- Loss (treino vs validação)

## Dataset

**MNIST** (Modified National Institute of Standards and Technology):
- 60.000 imagens de treino
- 10.000 imagens de teste
- 10 classes (dígitos 0-9)
- Imagens em escala de cinza 28x28 pixels

O dataset é carregado automaticamente via `tf.keras.datasets.mnist`.

**Nota**: Este projeto foi criado para fins educacionais e demonstração de boas práticas em projetos de Deep Learning.
