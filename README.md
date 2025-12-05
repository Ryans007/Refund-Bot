# Agente de Reembolso - POC com RAG

## Descrição

POC de agente interno para decisões de reembolso/cancelamento utilizando RAG (Retrieval-Augmented Generation) com base de conhecimento simulada. O sistema foi desenvolvido com foco em consistência operacional e redução de respostas incorretas.

### Características Principais

- **RAG (Retrieval-Augmented Generation)**: Utiliza uma base de conhecimento para fundamentar as decisões
- **Sistema de Confiança**: Implementa fallback automático para respostas com baixa confiança
- **Cenários Críticos Testados**:
  - Pedido já saiu para entrega
  - Cancelamento por falha do restaurante
  - Cobrança após cancelamento
- **Arquitetura Multi-Agente**: Sistema baseado em LangGraph com agentes especializados
- **Vector Store**: Busca semântica usando FAISS

## Tecnologias Utilizadas

- **Python 3.11**
- **FastAPI**: API REST para comunicação com o sistema
- **PostgreSQL**: Banco de dados para armazenamento de histórico
- **Docker & Docker Compose**: Containerização e orquestração
- **LangChain** & **LangGraph**: Framework para agentes e orquestração
- **Google Gemini**: Modelos de linguagem (2.5-pro e 2.5-flash)
- **FAISS**: Vector store para busca semântica
- **SQLAlchemy**: ORM para interação com banco de dados
- **Pydantic**: Validação de dados estruturados

## Como Instalar

### Pré-requisitos

- **Docker** e **Docker Compose** instalados
- Conta no Google AI Studio para obter API Key do Gemini


### Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd "Agente de Rembolso"
```

2. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```env
# API do Google Gemini
GEMINI_API_KEY=sua_chave_api_aqui

# Configurações do PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=reembolso_db
POSTGRES_PORT=5432

# Porta do backend
BACKEND_PORT=8000
```

> **Nota**: Obtenha sua API Key em [Google AI Studio](https://aistudio.google.com/apikey)

3. **Execute com Docker Compose**
```bash
docker-compose up -d --build
```

4. **Acesse a aplicação**
- API: http://localhost:8000
- Documentação da API: http://localhost:8000/docs

### Instalação para Desenvolvimento Local

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd "Agente de Rembolso"
```

2. **Crie e ative um ambiente virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
cd backend
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente**

Crie um arquivo `.env` na raiz do projeto:
```env
GEMINI_API_KEY=sua_chave_api_aqui
```


5. **Prepare a base de conhecimento**

O sistema já inclui uma base de conhecimento de exemplo em `backend/data/base_conhecimento_ifood_genai-exemplo.csv`. O índice FAISS será criado automaticamente na primeira execução.

## Como Usar

1. **Inicie os serviços**
```bash
docker-compose up -d --build
```

2. **Acesse a documentação interativa**
Visite http://localhost:8000/docs para explorar a API

3. **Faça uma requisição de exemplo**
```bash
curl -X POST "http://localhost:8000/chat/" \
     -H "Content-Type: application/json" \
     -d '{"user_message": "O cliente quer reembolso, mas o pedido já saiu para entrega. Ainda é permitido?"}'
```

4. **Consulte o histórico de mensagens**
```bash
curl "http://localhost:8000/history/"
```


### Exemplos de Perguntas

- "O cliente pode pedir reembolso após o pedido sair para entrega?"
- "Houve falha do restaurante, o cliente tem direito a reembolso?"
- "O cliente foi cobrado após cancelar o pedido, e agora?"
- "Há situações em que o reembolso não se aplica?"

## Arquitetura do Sistema

### Fluxo de Processamento

```
Entrada do Usuário
    ↓
[Classification Agent] → Classifica a consulta
    ↓
[Reimbursement Agent] → Busca na base (RAG) + Gera resposta
    ↓
[Revisor Agent] → Valida confiança + Refina resposta
    ↓
Resposta Final
```

### Estrutura de Diretórios

```
backend/
├── index.py                     # API FastAPI (ponto de entrada)
├── test.py                      # Chatbot local
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Imagem Docker
├── assets/                      # Contém a imagem do grafo
├── data/                        # Base de conhecimento (CSV)
├── faiss_index/                 # Índices de busca vetorial
├── database/                    # Configuração do banco de dados
│   ├── database.py              # SQLAlchemy setup
│   └── checkpoints.db           # Base SQLite para checkpoints
├── models/                      # Modelos SQLAlchemy
│   └── message_model.py         # Modelo de mensagens
├── routes/                      # Rotas da API FastAPI
│   ├── chat_router.py           # Endpoint de chat
│   └── history_router.py        # Endpoint de histórico
├── schemes/                     # Schemas Pydantic
│   └── message_scheme.py        # Validação de dados
└── graph/
    ├── agents/                  # Definição dos agentes
    │   ├── classification_agent.py
    │   ├── reimbursement_agent.py
    │   └── revisor_agent.py
    ├── nodes/                   # Nós do grafo LangGraph
    │   ├── classification_node.py
    │   ├── reimbursement_node.py
    │   └── revisor_node.py
    ├── tools/                   # Ferramentas (vector store)
    │   └── vector_store_tool.py
    ├── graph.py                 # Orquestração do fluxo
    ├── state.py                 # Estado compartilhado
    ├── insertion.py             # Criação do vector store
    └── utils.py                 # Utilitários
```

## Sistema de Confiança

O agente utiliza um score de confiança (0.0 a 1.0) para avaliar suas respostas:

- **≥ 0.7**: Resposta considerada confiável
- **< 0.7**: Sistema aciona o revisor para refinamento
- **Fallback**: Sugere escalonamento humano quando necessário

## Personalização

### Atualizar Base de Conhecimento

1. Edite `backend/data/base_conhecimento_ifood_genai-exemplo.csv`
2. Adicione/modifique políticas no formato:
```csv
categoria,pergunta,resposta,fonte
reembolso,"Pergunta exemplo","Resposta exemplo","Política X.Y"
```
3. Delete `backend/faiss_index/` para forçar recriação do índice
4. Execute o sistema novamente

### Ajustar Modelos

No arquivo dos agentes (`backend/graph/agents/*.py`), você pode alterar:

```python
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-pro",  # ou "gemini-2.5-flash"
    temperature=0
)
```

## Visualização do Grafo

O sistema gera automaticamente uma visualização do fluxo dos agentes em `backend/assets/graph.png`.

## Licença

Este é um projeto de demonstração (POC).

---

