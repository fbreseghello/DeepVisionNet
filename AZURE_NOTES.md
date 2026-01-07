# Azure ML - Notas

## 📋 Sobre os Arquivos Azure

Este projeto contém templates para Azure Machine Learning que foram preservados da versão original:

### Arquivos:

1. **template.json** - Template ARM (Azure Resource Manager)
   - Define infraestrutura de computação
   - Especifica tipos de VM disponíveis
   - Configura autoscaling

2. **parameters.json** - Parâmetros de configuração
   - Local: Brazil South
   - Workspace: wkspc-1
   - Compute: cluster-ai-test
   - VM: Standard_DS11_v2

## 🚀 Uso (Opcional)

Se você deseja usar Azure ML:

### 1. Via Azure CLI:

```bash
# Login
az login

# Criar resource group
az group create --name rg-deepvisionnet --location brazilsouth

# Deploy usando template
az deployment group create \
  --resource-group rg-deepvisionnet \
  --template-file template.json \
  --parameters parameters.json
```

### 2. Via Portal Azure:

1. Acesse portal.azure.com
2. Vá para "Deploy a custom template"
3. Upload template.json
4. Preencha com valores de parameters.json
5. Review + Create

## 💰 Custos Estimados

Com a configuração atual (Standard_DS11_v2):
- **Modo Dedicado**: ~$0.28/hora
- **Com min_nodes=0**: Cobra apenas quando em uso
- **Autoscaling**: Economia significativa

## 🔧 Alternativas Locais

Para desenvolvimento local sem custos:

```bash
# Opção 1: CPU local (gratuito)
python DeepVisionNet.py

# Opção 2: Google Colab (gratuito com GPU)
# Upload o notebook para colab.research.google.com

# Opção 3: Kaggle Kernels (gratuito com GPU/TPU)
# Crie um kernel em kaggle.com
```

## ⚙️ Customização do Template

Para usar diferentes configurações:

### Mudar Região:
```json
"location": {
  "value": "eastus"  // Mais barato que brazilsouth
}
```

### Mudar VM:
```json
"vmSize": {
  "value": "Standard_NC6"  // GPU para deep learning
}
```

### Ajustar Autoscaling:
```json
"maxNodeCount": {"value": 4},  // Mais paralelismo
"minNodeCount": {"value": 0},  // Sem custo quando idle
"nodeIdleTimeBeforeScaleDown": {"value": "PT60S"}  // 60s idle
```

## 📊 Quando Usar Azure ML

✅ **Recomendado quando:**
- Datasets muito grandes (>10GB)
- Modelos complexos (>100M parâmetros)
- Treinamento distribuído necessário
- Produção enterprise
- CI/CD integrado
- Monitoramento centralizado

❌ **Não recomendado quando:**
- Projeto pessoal/estudos
- Dataset pequeno (MNIST = 50MB)
- Orçamento limitado
- Prototipagem rápida

## 🔐 Segurança

Se for usar em produção:

1. **Não commite credenciais** ao Git
2. Use **Azure Key Vault** para secrets
3. Configure **RBAC** (Role-Based Access Control)
4. Habilite **Private Endpoints**
5. Configure **Network Security Groups**

## 📚 Recursos Azure ML

- [Documentação Oficial](https://docs.microsoft.com/azure/machine-learning/)
- [Pricing Calculator](https://azure.microsoft.com/pricing/calculator/)
- [VM Sizes](https://docs.microsoft.com/azure/virtual-machines/sizes)

---

**Nota**: Os templates Azure ML são **opcionais**. O projeto funciona perfeitamente sem eles usando apenas Python local.
