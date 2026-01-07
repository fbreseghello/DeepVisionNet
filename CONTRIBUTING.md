# 🤝 Guia de Contribuição - DeepVisionNet

Obrigado por considerar contribuir com o DeepVisionNet! Este documento fornece diretrizes para contribuições.

## 📋 Sumário

1. [Como Posso Contribuir?](#como-posso-contribuir)
2. [Processo de Desenvolvimento](#processo-de-desenvolvimento)
3. [Padrões de Código](#padrões-de-código)
4. [Commit Guidelines](#commit-guidelines)
5. [Pull Request Process](#pull-request-process)
6. [Reportar Bugs](#reportar-bugs)
7. [Sugerir Melhorias](#sugerir-melhorias)

---

## 🎯 Como Posso Contribuir?

### 1. Reportar Bugs
- Use a aba Issues no GitHub
- Descreva o problema detalhadamente
- Inclua passos para reproduzir
- Adicione screenshots se aplicável

### 2. Sugerir Features
- Abra uma Issue com tag `enhancement`
- Explique o caso de uso
- Descreva a solução proposta
- Discuta alternativas

### 3. Melhorar Documentação
- Corrigir typos
- Adicionar exemplos
- Clarificar instruções
- Traduzir documentos

### 4. Contribuir com Código
- Implementar features
- Corrigir bugs
- Otimizar performance
- Adicionar testes

---

## 🔧 Processo de Desenvolvimento

### Setup do Ambiente

```bash
# 1. Fork o repositório
# Clique em "Fork" no GitHub

# 2. Clone seu fork
git clone https://github.com/SEU-USUARIO/DeepVisionNet.git
cd DeepVisionNet

# 3. Adicione o upstream
git remote add upstream https://github.com/ORIGINAL/DeepVisionNet.git

# 4. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 5. Instale dependências
pip install -r requirements.txt
pip install pytest black flake8  # Dev dependencies

# 6. Crie uma branch para sua feature
git checkout -b feature/minha-feature
```

### Workflow de Desenvolvimento

```bash
# 1. Mantenha seu fork atualizado
git fetch upstream
git merge upstream/main

# 2. Faça suas alterações
# ... código ...

# 3. Execute os testes
pytest test_deepvisionnet.py -v

# 4. Formate o código
black DeepVisionNet.py
black example_advanced.py

# 5. Verifique linting
flake8 DeepVisionNet.py --max-line-length=100

# 6. Commit suas mudanças
git add .
git commit -m "feat: adiciona nova funcionalidade X"

# 7. Push para seu fork
git push origin feature/minha-feature

# 8. Abra um Pull Request no GitHub
```

---

## 📝 Padrões de Código

### Python Style Guide

Seguimos [PEP 8](https://pep8.org/) com algumas adaptações:

```python
# ✅ BOM
def calculate_accuracy(predictions, labels):
    """
    Calcula a acurácia das predições.
    
    Args:
        predictions (np.ndarray): Predições do modelo
        labels (np.ndarray): Labels verdadeiros
        
    Returns:
        float: Acurácia entre 0 e 1
    """
    correct = (predictions == labels).sum()
    total = len(labels)
    return correct / total


# ❌ RUIM
def calc_acc(p, l):  # Nomes não descritivos
    return sum([1 for i in range(len(p)) if p[i]==l[i]])/len(p)  # Sem espaços
```

### Docstrings

Use docstrings no estilo Google:

```python
def exemplo_funcao(param1, param2):
    """
    Breve descrição da função.
    
    Descrição mais detalhada se necessário.
    Pode ter múltiplas linhas.
    
    Args:
        param1 (tipo): Descrição do parâmetro 1
        param2 (tipo): Descrição do parâmetro 2
        
    Returns:
        tipo: Descrição do retorno
        
    Raises:
        ExceptionType: Quando ocorre X
        
    Example:
        >>> exemplo_funcao(1, 2)
        3
    """
    pass
```

### Naming Conventions

```python
# Classes: PascalCase
class DeepVisionNet:
    pass

# Funções e variáveis: snake_case
def train_model():
    learning_rate = 0.001

# Constantes: UPPER_CASE
MAX_EPOCHS = 100
DEFAULT_BATCH_SIZE = 128

# Privados: _prefixo
def _internal_function():
    pass
```

---

## 📨 Commit Guidelines

### Formato

```
<tipo>(<escopo>): <descrição curta>

<descrição detalhada opcional>

<footer opcional>
```

### Tipos

- `feat`: Nova funcionalidade
- `fix`: Correção de bug
- `docs`: Alterações na documentação
- `style`: Formatação, ponto e vírgula, etc
- `refactor`: Refatoração de código
- `test`: Adição ou modificação de testes
- `chore`: Tarefas de build, configs, etc
- `perf`: Melhoria de performance

### Exemplos

```bash
# Feature
git commit -m "feat(model): adiciona suporte para data augmentation"

# Bug fix
git commit -m "fix(training): corrige cálculo de validation split"

# Documentação
git commit -m "docs(readme): atualiza instruções de instalação"

# Refatoração
git commit -m "refactor(callbacks): simplifica configuração de callbacks"

# Testes
git commit -m "test(model): adiciona teste para build_model()"
```

---

## 🔀 Pull Request Process

### Checklist

Antes de abrir um PR, verifique:

- [ ] Código segue os padrões do projeto
- [ ] Testes estão passando (`pytest -v`)
- [ ] Código formatado (`black .`)
- [ ] Linting sem erros (`flake8`)
- [ ] Documentação atualizada
- [ ] Changelog atualizado (se aplicável)
- [ ] Commit messages seguem o padrão
- [ ] Branch atualizada com main

### Template de PR

```markdown
## Descrição
Breve descrição das mudanças

## Tipo de Mudança
- [ ] Bug fix
- [ ] Nova feature
- [ ] Breaking change
- [ ] Documentação

## Como Foi Testado?
Descreva os testes realizados

## Checklist
- [ ] Testes passando
- [ ] Código formatado
- [ ] Documentação atualizada
- [ ] Sem warnings de linting

## Screenshots (se aplicável)
```

### Processo de Review

1. **Submissão**: Você abre o PR
2. **Review Automático**: CI/CD roda testes
3. **Code Review**: Mantenedor revisa o código
4. **Feedback**: Mudanças podem ser solicitadas
5. **Aprovação**: PR é aprovado
6. **Merge**: Código é integrado ao main

---

## 🐛 Reportar Bugs

### Template de Bug Report

```markdown
**Descrição do Bug**
Descrição clara e concisa do bug.

**Para Reproduzir**
Passos para reproduzir:
1. Execute '...'
2. Configure '....'
3. Observe o erro

**Comportamento Esperado**
O que deveria acontecer.

**Screenshots**
Se aplicável, adicione screenshots.

**Ambiente**
 - OS: [e.g. Windows 10]
 - Python: [e.g. 3.9]
 - TensorFlow: [e.g. 2.15.0]

**Contexto Adicional**
Qualquer outra informação relevante.
```

---

## 💡 Sugerir Melhorias

### Template de Feature Request

```markdown
**Problema que Resolve**
Descrição clara do problema que a feature resolve.

**Solução Proposta**
Descrição da solução que você gostaria.

**Alternativas Consideradas**
Outras soluções que você considerou.

**Contexto Adicional**
Screenshots, exemplos, referências, etc.
```

---

## 🧪 Testes

### Escrever Testes

```python
import pytest
from DeepVisionNet import DeepVisionNet

def test_minha_feature():
    """Testa a feature X."""
    dvn = DeepVisionNet()
    resultado = dvn.minha_feature()
    assert resultado == valor_esperado
```

### Executar Testes

```bash
# Todos os testes
pytest -v

# Teste específico
pytest test_deepvisionnet.py::TestDeepVisionNet::test_build_model -v

# Com coverage
pytest --cov=DeepVisionNet --cov-report=html
```

---

## 📚 Recursos

### Documentação
- [README.md](README.md) - Introdução geral
- [QUICKSTART.md](QUICKSTART.md) - Início rápido
- [ARCHITECTURE.md](ARCHITECTURE.md) - Arquitetura detalhada
- [IMPROVEMENTS.md](IMPROVEMENTS.md) - Melhorias implementadas

### Ferramentas Úteis
- [Black](https://black.readthedocs.io/) - Formatador de código
- [Flake8](https://flake8.pycqa.org/) - Linter
- [pytest](https://docs.pytest.org/) - Framework de testes
- [TensorFlow Docs](https://www.tensorflow.org/api_docs) - Referência TF

---

## ❓ Dúvidas?

- 📧 Email: seu-email@exemplo.com
- 💬 Discord: [Link do servidor]
- 🐦 Twitter: [@seu-usuario]
- 💼 LinkedIn: [Seu perfil]

---

## 📜 Código de Conduta

### Nossa Promessa

Nós, como membros, contribuidores e líderes, nos comprometemos a fazer da participação em nossa comunidade uma experiência livre de assédio para todos.

### Padrões

Exemplos de comportamento que contribuem para um ambiente positivo:

✅ Usar linguagem acolhedora e inclusiva
✅ Ser respeitoso com diferentes pontos de vista
✅ Aceitar críticas construtivas graciosamente
✅ Focar no que é melhor para a comunidade
✅ Mostrar empatia com outros membros

❌ Não usar linguagem ou imagens sexualizadas
❌ Não fazer comentários insultuosos ou depreciativos
❌ Não realizar assédio público ou privado
❌ Não publicar informações privadas de outros

### Aplicação

Comportamentos inaceitáveis podem ser reportados para os mantenedores do projeto. Todas as reclamações serão revisadas e investigadas.

---

## 🎉 Agradecimentos

Obrigado por contribuir com o DeepVisionNet! Sua ajuda torna este projeto melhor para todos.

### Hall da Fama dos Contribuidores

<!-- Será atualizado automaticamente -->

---

**Última Atualização**: Janeiro 2026  
**Versão**: 1.0.0
