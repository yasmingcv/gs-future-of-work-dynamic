# 🎯 Otimizador de Requalificação - Global Solution

## 📋 Descrição

Este projeto implementa um sistema de otimização para requalificação profissional utilizando **Programação Dinâmica**. O sistema resolve o problema clássico da **Mochila 0/1 (Knapsack Problem)** para recomendar a melhor combinação de cursos que maximize o impacto na carreira dentro de um limite de tempo disponível para estudos.

## 🚀 Funcionalidades

- **Catálogo de Cursos**: Cursos divididos em diferentes categorias (IA, Dados, etc.)
- **Otimização Inteligente**: Duas implementações de programação dinâmica:
  - **Memoização (Top-Down)**: Abordagem recursiva com cache
  - **Tabulação (Bottom-Up)**: Abordagem iterativa com matriz DP
- **Interface Interativa**: Console amigável para inserir tempo disponível
- **Validação Cruzada**: Verificação automática de consistência entre os dois algoritmos
- **Relatórios Detalhados**: Exibição completa dos cursos recomendados com impacto e categorias

## 📁 Estrutura do Projeto

```
gs-dynamic-programming/
├── app.py                     # Aplicação principal
├── courses_reskilling.json    # Catálogo de cursos
└── README.md                  # Documentação
```

## 🔧 Tecnologias Utilizadas

- **Python 3.x**
- **JSON** (para armazenamento de dados)
- **Programação Dinâmica** (algoritmos de otimização)

## 📊 Formato dos Dados

Cada curso no arquivo `courses_reskilling.json` contém:

```json
{
  "id": 1,
  "name": "IA Generativa",
  "hours": 80,
  "impact": 90,
  "category": "Inteligência Artificial",
  "description": "Conceitos básicos de modelos generativos...",
  "prerequisites": ["Lógica básica de programação"]
}
```

## 🎮 Como Usar

### 1. Pré-requisitos
- Python 3.6 ou superior instalado
- Arquivo `courses_reskilling.json` no mesmo diretório

### 2. Execução
```bash
python app.py
```

### 3. Interação
1. O sistema carregará o catálogo de cursos
2. Digite o número de horas disponíveis para estudo
3. Aguarde o processamento dos algoritmos
4. Visualize os resultados otimizados

### 4. Exemplo de Saída
```
CATÁLOGO DE CURSOS PARA REQUALIFICAÇÃO
================================================================================
Nome do Curso                    Horas  Impacto Categoria
--------------------------------------------------------------------------------
IA Generativa                       80       90  Inteligência Artificial
Análise de Dados                   120       85  Dados
...

Quantas horas você tem disponíveis para estudar? 200

RESULTADO - MEMOIZAÇÃO (Top-Down)
Impacto Máximo Alcançado: 175 pontos
Horas utilizadas: 200h
Cursos recomendados:
--------------------------------------------------
  • IA Generativa (80h) → Impacto: 90 | Inteligência Artificial
  • Análise de Dados (120h) → Impacto: 85 | Dados
--------------------------------------------------
```

## 🧠 Algoritmos Implementados

### 1. Memoização (Top-Down)
- **Complexidade**: O(n × W)
- **Espaço**: O(n × W) para cache + O(n) para recursão
- **Vantagem**: Mais intuitivo e próximo da definição matemática

### 2. Tabulação (Bottom-Up)
- **Complexidade**: O(n × W)
- **Espaço**: O(n × W) para matriz DP
- **Vantagem**: Sem risco de stack overflow, mais eficiente em memória

Onde:
- **n** = número de cursos
- **W** = capacidade da mochila (horas disponíveis)

## 👥 Integrantes

- **David Murillo de Oliveira Soares** (RM 559078)
- **Lucas Serrano Rocco** (RM 555170)
- **Yasmin Gonçalves Coelho** (RM 559147)