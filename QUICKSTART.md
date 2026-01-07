### Clone e Navegue
```bash
git clone https://github.com/seu-usuario/DeepVisionNet.git
cd DeepVisionNet
```

### Instale Dependências
```bash
# Crie ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale pacotes
pip install -r requirements.txt
```

### Execute!
```bash
python DeepVisionNet.py
```

---

## Uso Rápido

### Treinamento Padrão (20 épocas)
```bash
python DeepVisionNet.py
```

**Saída**: Arquivos em `results/`
- Modelo salvo
- Gráficos de treinamento
- Logs completos

### Treinamento Rápido (5 épocas para teste)
```bash
python DeepVisionNet.py --epochs 5
```

### Treinamento de Alta Performance
```bash
python DeepVisionNet.py --epochs 50 --batch-size 256 --learning-rate 0.0005
```

---

## O Que Esperar

### Tempo de Execução:
- **CPU**: ~3-5 minutos (20 épocas)
- **GPU**: ~30-60 segundos (20 épocas)

### Resultados:
- **Acurácia**: ~99.0-99.5%
- **Loss**: ~0.03-0.05

### Arquivos Gerados:
```
results/
├── model_best_*.keras        # ← Use este modelo!
├── model_final.keras
├── training_history.png      # ← Visualize os resultados
├── training_log_*.csv
└── model_summary.txt
```

---

## Verificar Resultados

### 1. Visualizar Gráficos
Abra o arquivo: `results/training_history.png`

### 2. Ver Log de Treinamento
```bash
cat training.log  # Linux/Mac
type training.log  # Windows
```

### 3. Carregar Modelo Salvo
```python
from tensorflow import keras

model = keras.models.load_model('results/model_best_*.keras')
print(model.summary())
```

---

## Testar o Código

```bash
# Instale pytest (se ainda não instalou)
pip install pytest

# Execute os testes
pytest test_deepvisionnet.py -v
```

**Resultado esperado**: ✅ 11 testes passando

---

## Casos de Uso Comuns

### 1. Experimentar com Learning Rate
```bash
# Learning rate baixo (treinamento lento mas estável)
python DeepVisionNet.py --learning-rate 0.0001

# Learning rate alto (treinamento rápido mas pode divergir)
python DeepVisionNet.py --learning-rate 0.01
```

### 2. Testar Batch Sizes
```bash
# Batch pequeno (mais atualizações, mais lento)
python DeepVisionNet.py --batch-size 32

# Batch grande (menos atualizações, mais rápido)
python DeepVisionNet.py --batch-size 512
```

### 3. Comparar Configurações
```bash
# Experimento 1
python DeepVisionNet.py --output-dir exp1 --epochs 20

# Experimento 2
python DeepVisionNet.py --output-dir exp2 --epochs 30 --learning-rate 0.0005

# Experimento 3
python DeepVisionNet.py --output-dir exp3 --batch-size 64
```

---

## Resolução de Problemas

### Erro: "No module named 'tensorflow'"
```bash
pip install tensorflow
```

### Erro: "No module named 'matplotlib'"
```bash
pip install matplotlib
```

### Erro: "Out of memory"
```bash
# Reduza o batch size
python DeepVisionNet.py --batch-size 32
```

### Warning sobre GPU não encontrada
**Normal!** O código funciona em CPU também.

Para usar GPU:
1. Instale CUDA e cuDNN
2. Instale: `pip install tensorflow-gpu`

### Modelo não está aprendendo
- Verifique se o learning rate não está muito alto
- Tente: `--learning-rate 0.001` (padrão)
- Aumente épocas: `--epochs 30`

---

## Próximos Passos

1. Execute o treinamento básico
2. Analise os gráficos gerados
3. Execute os testes
4. Experimente com diferentes hiperparâmetros
5. Veja `example_advanced.py` para uso avançado
6. Leia `IMPROVEMENTS.md` para entender as melhorias

---

## Dicas Profissionais

### 1. Use EarlyStopping
**Já configurado!** O treinamento para automaticamente se não houver melhoria.

### 2. Monitore a Diferença Train/Validation
Se treino >> validação = **overfitting**
- Solução: Aumentar dropout ou adicionar regularização

### 3. Salve Experimentos
```bash
mkdir experiments
python DeepVisionNet.py --output-dir experiments/exp1
python DeepVisionNet.py --output-dir experiments/exp2 --learning-rate 0.0005
```

### 4. Compare Resultados
```python
import pandas as pd

exp1 = pd.read_csv('experiments/exp1/training_log_*.csv')
exp2 = pd.read_csv('experiments/exp2/training_log_*.csv')

print(exp1['val_accuracy'].max())
print(exp2['val_accuracy'].max())
```