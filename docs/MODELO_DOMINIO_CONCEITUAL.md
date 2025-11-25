# Modelo de Domínio Conceitual - CareerConnectAI

## Visão Geral

O CareerConnectAI é um sistema de gerenciamento de trilhas de carreira que permite aos usuários escolherem entre trilhas pré-definidas ou solicitar trilhas personalizadas geradas por LLM (Large Language Model).

## Entidades Principais

### 1. Usuário (CustomUser)
**Descrição:** Representa um usuário do sistema, que pode ser um estudante ou administrador.

**Atributos:**
- `email` (String, único, obrigatório): Email do usuário usado para login
- `username` (String): Nome de usuário
- `password` (String, hash): Senha criptografada
- `is_staff` (Boolean): Indica se é administrador
- `is_active` (Boolean): Indica se a conta está ativa
- `date_joined` (DateTime): Data de criação da conta
- `last_login` (DateTime): Último acesso ao sistema

**Relacionamentos:**
- Possui um `ProgressoUsuario` (1:1)
- Pode ter múltiplas trilhas personalizadas (1:N)

### 2. Área (Area)
**Descrição:** Representa uma categoria ou área de carreira (ex: "Desenvolvimento Web", "Ciência de Dados").

**Atributos:**
- `nome` (String, único, obrigatório): Nome da área de carreira

**Relacionamentos:**
- Possui múltiplas `Trilhas` (1:N)

### 3. Trilha (Trilha)
**Descrição:** Representa uma trilha de carreira completa, que pode ser pré-definida ou personalizada.

**Atributos:**
- `titulo` (String, obrigatório): Título da trilha
- `descricao` (Text): Descrição detalhada da trilha
- `area` (ForeignKey → Area): Área de carreira à qual pertence
- `tipo` (Enum): Tipo da trilha - "PREDEFINIDA" ou "PERSONALIZADA"
- `criado_por` (ForeignKey → CustomUser, opcional): Usuário que criou (se personalizada)
- `data_criacao` (DateTime): Data de criação
- `is_ativa` (Boolean): Indica se a trilha está ativa

**Relacionamentos:**
- Pertence a uma `Area` (N:1)
- Possui múltiplas `Etapas` (1:N)
- Pode ser selecionada por múltiplos `ProgressoUsuario` (N:N)

### 4. Etapa (Etapa)
**Descrição:** Representa um passo ou etapa dentro de uma trilha.

**Atributos:**
- `trilha` (ForeignKey → Trilha): Trilha à qual pertence
- `titulo` (String, obrigatório): Título da etapa
- `descricao` (Text): Descrição detalhada da etapa
- `ordem` (Integer, obrigatório): Ordem sequencial da etapa na trilha
- `data_criacao` (DateTime): Data de criação

**Relacionamentos:**
- Pertence a uma `Trilha` (N:1)
- Pode ser concluída por múltiplos usuários (N:N via ProgressoUsuario)

### 5. ProgressoUsuario (ProgressoUsuario)
**Descrição:** Rastreia o progresso de um usuário em suas trilhas.

**Atributos:**
- `usuario` (OneToOne → CustomUser): Usuário dono do progresso
- `trilha_selecionada` (ForeignKey → Trilha, opcional): Trilha atualmente selecionada
- `data_selecao` (DateTime): Data em que a trilha foi selecionada
- `porcentagem_conclusao` (Float, calculado): Porcentagem de etapas concluídas

**Relacionamentos:**
- Pertence a um `CustomUser` (1:1)
- Referencia uma `Trilha` (N:1)
- Possui múltiplas `Etapas` concluídas (N:N)

### 6. TrilhaPersonalizada (Conceitual)
**Descrição:** Representa uma trilha gerada por LLM baseada em requisitos do usuário.

**Atributos:**
- `requisitos_usuario` (Text): Requisitos fornecidos pelo usuário
- `prompt_llm` (Text): Prompt enviado ao LLM
- `resposta_llm` (Text): Resposta recebida do LLM
- `data_geracao` (DateTime): Data de geração
- `status` (Enum): "PENDENTE", "GERANDO", "CONCLUIDA", "ERRO"

**Relacionamentos:**
- Herda de `Trilha` (tipo = "PERSONALIZADA")
- Criada por um `CustomUser` (N:1)

## Relacionamentos Principais

```
CustomUser (1) ──────── (1) ProgressoUsuario
    │                          │
    │                          │
    │                          └─── (N) Trilha (selecionada)
    │
    └─── (N) Trilha (criadas - personalizadas)

Area (1) ──────── (N) Trilha

Trilha (1) ──────── (N) Etapa

ProgressoUsuario (N) ──────── (N) Etapa (concluídas)
```

## Regras de Negócio

1. **Autenticação:**
   - Login é realizado exclusivamente via email
   - Senha deve ser criptografada
   - Sessões devem ser gerenciadas adequadamente

2. **Trilhas:**
   - Trilhas pré-definidas são criadas apenas por administradores
   - Trilhas personalizadas são criadas por usuários via LLM
   - Uma trilha deve ter pelo menos uma etapa
   - A ordem das etapas deve ser única dentro de uma trilha

3. **Progresso:**
   - Um usuário pode ter apenas uma trilha selecionada por vez
   - Etapas só podem ser concluídas se pertencerem à trilha selecionada
   - A porcentagem de conclusão é calculada automaticamente

4. **LLM:**
   - Trilhas personalizadas são geradas assincronamente
   - O sistema deve validar a resposta do LLM antes de criar a trilha
   - Em caso de erro, o usuário deve ser notificado

## Diagrama de Classes Conceitual

```
┌─────────────────────┐
│    CustomUser       │
├─────────────────────┤
│ + email: String     │
│ + username: String  │
│ + password: Hash    │
│ + is_staff: Boolean │
└──────────┬──────────┘
           │ 1
           │
           │ 1
┌──────────▼──────────┐
│ ProgressoUsuario    │
├─────────────────────┤
│ + trilha_selecionada│
│ + etapas_concluidas │
└──────────┬──────────┘
           │ N
           │
           │ 1
┌──────────▼──────────┐
│      Trilha         │
├─────────────────────┤
│ + titulo: String    │
│ + descricao: Text   │
│ + tipo: Enum        │
└──────────┬──────────┘
           │ 1
           │
           │ N
┌──────────▼──────────┐
│       Etapa         │
├─────────────────────┤
│ + titulo: String    │
│ + descricao: Text   │
│ + ordem: Integer    │
└─────────────────────┘

┌─────────────────────┐
│       Area          │
├─────────────────────┤
│ + nome: String      │
└──────────┬──────────┘
           │ 1
           │
           │ N
┌──────────▼──────────┐
│      Trilha         │
└─────────────────────┘
```


