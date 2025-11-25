# Diagramas - CareerConnectAI

## Diagrama de Casos de Uso

```mermaid
graph TB
    Usuario[👤 Usuário]
    Admin[👨‍💼 Administrador]
    Sistema[💻 Sistema CareerConnectAI]
    LLM[🤖 Serviço LLM]
    
    Usuario -->|Login e Autenticação| Sistema
    Usuario -->|Visualizar Trilha e Progresso| Sistema
    Usuario -->|Escolher Trilha Pré-definida| Sistema
    Usuario -->|Solicitar Trilha Personalizada| Sistema
    Sistema -->|Gerar Trilha| LLM
    Usuario -->|Marcar Etapa como Concluída| Sistema
    
    Admin -->|Gerenciar Categorias| Sistema
    Admin -->|Gerenciar Trilhas| Sistema
    Admin -->|Gerenciar Etapas| Sistema
```

## Diagrama de Classes do Domínio

```mermaid
classDiagram
    class CustomUser {
        +String email
        +String username
        +String password
        +Boolean is_staff
        +Boolean is_active
        +DateTime date_joined
        +DateTime last_login
    }
    
    class Area {
        +String nome
    }
    
    class Trilha {
        +String titulo
        +Text descricao
        +Enum tipo
        +DateTime data_criacao
        +Boolean is_ativa
    }
    
    class Etapa {
        +String titulo
        +Text descricao
        +Integer ordem
        +DateTime data_criacao
    }
    
    class ProgressoUsuario {
        +DateTime data_selecao
        +Float porcentagem_conclusao
    }
    
    CustomUser "1" --> "1" ProgressoUsuario : possui
    ProgressoUsuario "N" --> "1" Trilha : seleciona
    ProgressoUsuario "N" --> "N" Etapa : conclui
    Area "1" --> "N" Trilha : contém
    Trilha "1" --> "N" Etapa : possui
    CustomUser "1" --> "N" Trilha : cria (personalizadas)
```

## Diagrama de Sequência - Login

```mermaid
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant A as Autenticação
    participant BD as Banco de Dados
    
    U->>S: Acessa página de login
    S->>U: Exibe formulário
    U->>S: Informa email e senha
    S->>A: Valida credenciais
    A->>BD: Consulta usuário
    BD->>A: Retorna dados do usuário
    A->>S: Credenciais válidas
    S->>S: Cria sessão
    S->>U: Redireciona para dashboard
```

## Diagrama de Sequência - Solicitar Trilha Personalizada

```mermaid
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant LLM as Serviço LLM
    participant BD as Banco de Dados
    
    U->>S: Acessa solicitar trilha
    S->>U: Exibe formulário
    U->>S: Preenche requisitos
    S->>BD: Cria registro (status PENDENTE)
    S->>U: Mensagem "Gerando..."
    S->>LLM: Envia prompt estruturado
    LLM->>LLM: Processa requisição
    LLM->>S: Retorna JSON com trilha
    S->>S: Valida resposta
    alt Resposta válida
        S->>BD: Cria Trilha e Etapas
        S->>BD: Atualiza ProgressoUsuario
        S->>U: Notifica sucesso
        S->>U: Redireciona para trilha
    else Resposta inválida
        S->>BD: Atualiza status (ERRO)
        S->>U: Exibe mensagem de erro
    end
```

## Diagrama de Sequência - Marcar Etapa Concluída

```mermaid
sequenceDiagram
    participant U as Usuário
    participant S as Sistema
    participant BD as Banco de Dados
    
    U->>S: Visualiza trilha
    S->>BD: Busca trilha e progresso
    BD->>S: Retorna dados
    S->>U: Exibe etapas
    U->>S: Clica "Marcar como concluída"
    S->>BD: Valida etapa
    BD->>S: Validação OK
    S->>BD: Adiciona à etapas_concluidas
    S->>BD: Recalcula porcentagem
    BD->>S: Retorna progresso atualizado
    S->>U: Atualiza interface
```

## Diagrama de Estados - Trilha Personalizada

```mermaid
stateDiagram-v2
    [*] --> Pendente: Usuário solicita
    Pendente --> Gerando: Sistema inicia geração
    Gerando --> Concluida: LLM retorna com sucesso
    Gerando --> Erro: LLM falha ou timeout
    Erro --> Pendente: Usuário tenta novamente
    Concluida --> [*]: Trilha criada
```

## Diagrama de Atividades - Fluxo Completo do Usuário

```mermaid
flowchart TD
    Start([Usuário acessa sistema]) --> Login{Está autenticado?}
    Login -->|Não| LoginPage[Página de Login]
    LoginPage --> Autentica{Autenticação OK?}
    Autentica -->|Não| LoginPage
    Autentica -->|Sim| Dashboard
    Login -->|Sim| Dashboard[Dashboard]
    
    Dashboard --> TemTrilha{Tem trilha selecionada?}
    TemTrilha -->|Não| EscolherTrilha[Escolher Trilha]
    TemTrilha -->|Sim| VisualizarTrilha[Visualizar Trilha]
    
    EscolherTrilha --> TipoTrilha{Tipo de trilha?}
    TipoTrilha -->|Pré-definida| ListaPredefinidas[Listar Trilhas Pré-definidas]
    TipoTrilha -->|Personalizada| SolicitarPersonalizada[Solicitar Trilha Personalizada]
    
    ListaPredefinidas --> SelecionaPredefinida[Seleciona Trilha]
    SelecionaPredefinida --> VisualizarTrilha
    
    SolicitarPersonalizada --> PreencheRequisitos[Preenche Requisitos]
    PreencheRequisitos --> GeraLLM[Gera via LLM]
    GeraLLM --> SucessoLLM{Sucesso?}
    SucessoLLM -->|Sim| VisualizarTrilha
    SucessoLLM -->|Não| ErroLLM[Exibe Erro]
    ErroLLM --> SolicitarPersonalizada
    
    VisualizarTrilha --> VerEtapas[Visualiza Etapas]
    VerEtapas --> MarcarEtapa[Marcar Etapa Concluída]
    MarcarEtapa --> AtualizaProgresso[Atualiza Progresso]
    AtualizaProgresso --> TodasConcluidas{Todas concluídas?}
    TodasConcluidas -->|Não| VerEtapas
    TodasConcluidas -->|Sim| Parabens[Exibe Parabéns]
    Parabens --> Dashboard
```

## Diagrama de Componentes

```mermaid
graph TB
    subgraph "Frontend"
        UI[Interface do Usuário]
        AdminUI[Interface Admin]
    end
    
    subgraph "Backend - Django"
        Views[Views/Controllers]
        Models[Models]
        Serializers[Serializers]
        Admin[Admin Panel]
    end
    
    subgraph "Serviços"
        AuthService[Serviço de Autenticação]
        LLMService[Serviço LLM]
    end
    
    subgraph "Banco de Dados"
        DB[(SQLite/PostgreSQL)]
    end
    
    UI --> Views
    AdminUI --> Admin
    Admin --> Models
    Views --> Models
    Views --> Serializers
    Views --> AuthService
    Views --> LLMService
    Models --> DB
    AuthService --> DB
    LLMService --> LLM[API Externa LLM]
```

## Diagrama de Entidade-Relacionamento (ER)

```mermaid
erDiagram
    CUSTOMUSER ||--|| PROGRESSOUSUARIO : possui
    CUSTOMUSER ||--o{ TRILHA : cria
    AREA ||--o{ TRILHA : contém
    TRILHA ||--o{ ETAPA : possui
    PROGRESSOUSUARIO }o--|| TRILHA : seleciona
    PROGRESSOUSUARIO }o--o{ ETAPA : conclui
    
    CUSTOMUSER {
        int id PK
        string email UK
        string username
        string password
        boolean is_staff
        boolean is_active
        datetime date_joined
        datetime last_login
    }
    
    AREA {
        int id PK
        string nome UK
    }
    
    TRILHA {
        int id PK
        string titulo
        text descricao
        enum tipo
        int area_id FK
        int criado_por_id FK
        datetime data_criacao
        boolean is_ativa
    }
    
    ETAPA {
        int id PK
        string titulo
        text descricao
        int ordem
        int trilha_id FK
        datetime data_criacao
    }
    
    PROGRESSOUSUARIO {
        int id PK
        int usuario_id FK
        int trilha_selecionada_id FK
        datetime data_selecao
        float porcentagem_conclusao
    }
```


