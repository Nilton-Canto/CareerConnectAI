# Casos de Uso - CareerConnectAI

## Índice

1. [Login e Autenticação do Usuário](#1-login-e-autenticação-do-usuário)
2. [Gerenciar Categorias, Trilhas e Etapas (Admin)](#2-gerenciar-categorias-trilhas-e-etapas-admin)
3. [Visualizar Trilha e Progresso](#3-visualizar-trilha-e-progresso)
4. [Escolher Trilha Pré-definida](#4-escolher-trilha-pré-definida)
5. [Solicitar Trilha Personalizada via LLM](#5-solicitar-trilha-personalizada-via-llm)
6. [Marcar Etapa como Concluída](#6-marcar-etapa-como-concluída)

---

## 1. Login e Autenticação do Usuário

### 1.1 Descrição
Permite que um usuário faça login no sistema usando email e senha, autenticando-se e obtendo acesso às funcionalidades do sistema.

### 1.2 Atores
- **Usuário:** Estudante ou administrador que deseja acessar o sistema

### 1.3 Pré-condições
- O usuário deve possuir uma conta cadastrada no sistema
- O email e senha devem estar corretos

### 1.4 Fluxo Principal
1. O usuário acessa a página de login
2. O sistema exibe o formulário de login (email e senha)
3. O usuário preenche email e senha
4. O usuário submete o formulário
5. O sistema valida as credenciais
6. O sistema autentica o usuário
7. O sistema cria uma sessão para o usuário
8. O sistema redireciona o usuário para a página inicial/dashboard
9. **Fim do caso de uso**

### 1.5 Fluxos Alternativos

#### 1.5.1 Credenciais Inválidas
- **3a.** Se email ou senha estiverem incorretos:
  1. O sistema exibe mensagem de erro: "Email ou senha inválidos"
  2. O sistema mantém o usuário na página de login
  3. Retorna ao passo 2 do fluxo principal

#### 1.5.2 Conta Inativa
- **3b.** Se a conta estiver inativa:
  1. O sistema exibe mensagem: "Conta inativa. Entre em contato com o suporte"
  2. O sistema mantém o usuário na página de login
  3. Retorna ao passo 2 do fluxo principal

#### 1.5.3 Recuperação de Senha
- **3c.** Se o usuário clicar em "Esqueci minha senha":
  1. O sistema redireciona para página de recuperação de senha
  2. O usuário informa o email
  3. O sistema envia email com link de recuperação
  4. O usuário redefine a senha
  5. Retorna ao passo 2 do fluxo principal

### 1.6 Pós-condições
- O usuário está autenticado no sistema
- Uma sessão foi criada
- O usuário tem acesso às funcionalidades conforme seu perfil (estudante/admin)

### 1.7 Regras de Negócio
- Login é realizado exclusivamente via email
- Senha deve ter no mínimo 8 caracteres
- Após 5 tentativas falhas, a conta é temporariamente bloqueada por 15 minutos
- Sessões expiram após 2 horas de inatividade

### 1.8 Diagrama de Sequência

```
Usuário          Sistema          Autenticação      Banco de Dados
  │                 │                    │                 │
  │─── Acessa ──────>│                    │                 │
  │                 │                    │                 │
  │<── Form Login ──│                    │                 │
  │                 │                    │                 │
  │─── Email/Senha ─>│                    │                 │
  │                 │                    │                 │
  │                 │─── Valida ────────>│                 │
  │                 │                    │                 │
  │                 │                    │─── Consulta ────>│
  │                 │                    │<── Usuário ─────│
  │                 │<── OK/NOK ────────│                 │
  │                 │                    │                 │
  │<── Dashboard ───│                    │                 │
  │                 │                    │                 │
```
link do miro : https://miro.com/app/board/uXjVJlBJpXs=/?share_link_id=55159032
---

## 2. Gerenciar Categorias, Trilhas e Etapas (Admin)

### 2.1 Descrição
Permite que um administrador gerencie (criar, editar, excluir, listar) categorias (áreas), trilhas pré-definidas e suas etapas.

### 2.2 Atores
- **Administrador:** Usuário com permissões de administrador

### 2.3 Pré-condições
- O usuário deve estar autenticado
- O usuário deve possuir permissões de administrador (`is_staff = True`)

### 2.4 Fluxo Principal - Criar Categoria
1. O administrador acessa o painel administrativo
2. O sistema exibe o menu de gerenciamento
3. O administrador seleciona "Gerenciar Categorias"
4. O sistema exibe a lista de categorias existentes
5. O administrador clica em "Nova Categoria"
6. O sistema exibe formulário de criação
7. O administrador preenche o nome da categoria
8. O administrador submete o formulário
9. O sistema valida os dados
10. O sistema cria a categoria
11. O sistema exibe mensagem de sucesso
12. O sistema redireciona para a lista de categorias
13. **Fim do caso de uso**

### 2.5 Fluxo Principal - Criar Trilha Pré-definida
1. O administrador acessa "Gerenciar Trilhas"
2. O sistema exibe a lista de trilhas
3. O administrador clica em "Nova Trilha"
4. O sistema exibe formulário de criação
5. O administrador preenche:
   - Título da trilha
   - Descrição
   - Seleciona a categoria/área
6. O administrador submete o formulário
7. O sistema valida os dados
8. O sistema cria a trilha (tipo = "PREDEFINIDA")
9. O sistema redireciona para adicionar etapas
10. O administrador adiciona etapas (ver 2.6)
11. **Fim do caso de uso**

### 2.6 Fluxo Principal - Criar Etapas
1. O administrador está na página de edição da trilha
2. O administrador clica em "Adicionar Etapa"
3. O sistema exibe formulário de etapa
4. O administrador preenche:
   - Título da etapa
   - Descrição
   - Ordem (número sequencial)
5. O administrador submete o formulário
6. O sistema valida os dados (verifica ordem única)
7. O sistema cria a etapa
8. O sistema atualiza a lista de etapas
9. O administrador pode adicionar mais etapas ou finalizar
10. **Fim do caso de uso**

### 2.7 Fluxos Alternativos

#### 2.7.1 Editar Categoria/Trilha/Etapa
- **2.7.1a.** Na lista, o administrador clica em "Editar":
  1. O sistema exibe formulário pré-preenchido
  2. O administrador modifica os dados
  3. O administrador salva
  4. O sistema valida e atualiza
  5. Retorna ao passo 12 do fluxo principal

#### 2.7.2 Excluir Categoria/Trilha/Etapa
- **2.7.2a.** Na lista, o administrador clica em "Excluir":
  1. O sistema solicita confirmação
  2. O administrador confirma
  3. O sistema verifica dependências:
     - Se categoria tem trilhas associadas → exibe erro
     - Se trilha tem usuários com progresso → exibe aviso
  4. O sistema exclui (ou marca como inativa)
  5. O sistema atualiza a lista

#### 2.7.3 Validação de Ordem de Etapas
- **2.7.3a.** Se a ordem informada já existir:
  1. O sistema exibe erro: "Ordem já existe. Escolha outra ordem"
  2. Retorna ao passo 4 do fluxo de criar etapas

### 2.8 Pós-condições
- A categoria/trilha/etapa foi criada/editada/excluída no sistema
- As alterações estão disponíveis para os usuários

### 2.9 Regras de Negócio
- Apenas administradores podem gerenciar categorias, trilhas e etapas
- Não é possível excluir uma categoria que possui trilhas associadas
- A ordem das etapas deve ser única dentro de uma trilha
- Uma trilha deve ter pelo menos uma etapa para ser considerada completa

---
link do miro: https://miro.com/app/board/uXjVJlBMXOE=/?share_link_id=371680571532

## 3. Visualizar Trilha e Progresso

### 3.1 Descrição
Permite que um usuário visualize a trilha selecionada e seu progresso atual, incluindo etapas concluídas e pendentes.

### 3.2 Atores
- **Usuário:** Estudante autenticado

### 3.3 Pré-condições
- O usuário deve estar autenticado
- O usuário deve ter uma trilha selecionada

### 3.4 Fluxo Principal
1. O usuário acessa a página "Minha Trilha" ou dashboard
2. O sistema verifica se há trilha selecionada
3. O sistema busca a trilha e o progresso do usuário
4. O sistema exibe:
   - Informações da trilha (título, descrição, área)
   - Lista de etapas ordenadas
   - Status de cada etapa (concluída/pendente)
   - Porcentagem de conclusão geral
   - Barra de progresso visual
5. O usuário pode clicar em uma etapa para ver detalhes
6. O sistema exibe detalhes da etapa selecionada
7. **Fim do caso de uso**

### 3.5 Fluxos Alternativos

#### 3.5.1 Usuário sem Trilha Selecionada
- **3.5.1a.** Se o usuário não tiver trilha selecionada:
  1. O sistema exibe mensagem: "Você ainda não selecionou uma trilha"
  2. O sistema oferece opções:
     - "Escolher Trilha Pré-definida"
     - "Solicitar Trilha Personalizada"
  3. O usuário escolhe uma opção
  4. Retorna ao caso de uso correspondente

#### 3.5.2 Filtrar Etapas
- **3.5.2a.** O usuário pode filtrar etapas:
  1. O usuário seleciona filtro (Todas/Concluídas/Pendentes)
  2. O sistema atualiza a lista conforme o filtro
  3. Retorna ao passo 4 do fluxo principal

### 3.6 Pós-condições
- O usuário visualizou sua trilha e progresso atual

### 3.7 Regras de Negócio
- A porcentagem de conclusão é calculada como: (etapas concluídas / total de etapas) * 100
- Etapas são exibidas sempre em ordem crescente
- Etapas concluídas são marcadas visualmente (check, cor diferente, etc.)

link miro: https://miro.com/app/board/uXjVJlBQua4=/?share_link_id=752965852198
---

## 4. Escolher Trilha Pré-definida

### 4.1 Descrição
Permite que um usuário escolha uma trilha pré-definida disponível no sistema para seguir.

### 4.2 Atores
- **Usuário:** Estudante autenticado

### 4.3 Pré-condições
- O usuário deve estar autenticado
- Deve existir pelo menos uma trilha pré-definida disponível

### 4.4 Fluxo Principal
1. O usuário acessa a página "Escolher Trilha"
2. O sistema busca todas as trilhas pré-definidas ativas
3. O sistema exibe as trilhas agrupadas por categoria/área
4. O usuário navega pelas categorias
5. O usuário visualiza detalhes de uma trilha (título, descrição, número de etapas)
6. O usuário seleciona uma trilha
7. O sistema solicita confirmação
8. O usuário confirma a seleção
9. O sistema verifica se o usuário já possui progresso:
   - Se sim, pergunta se deseja substituir a trilha atual
   - Se não, cria novo progresso
10. O sistema atualiza o `ProgressoUsuario` com a trilha selecionada
11. O sistema inicializa o progresso (nenhuma etapa concluída)
12. O sistema exibe mensagem de sucesso
13. O sistema redireciona para a visualização da trilha
14. **Fim do caso de uso**

### 4.5 Fluxos Alternativos

#### 4.5.1 Substituir Trilha Atual
- **4.5.1a.** Se o usuário já possui uma trilha selecionada:
  1. O sistema exibe aviso: "Você já possui uma trilha selecionada. Deseja substituir?"
  2. O usuário confirma
  3. O sistema remove etapas concluídas da trilha anterior
  4. O sistema atualiza para a nova trilha
  5. Retorna ao passo 10 do fluxo principal

#### 4.5.2 Cancelar Seleção
- **4.5.2a.** O usuário pode cancelar a seleção:
  1. O usuário clica em "Cancelar"
  2. O sistema retorna à lista de trilhas
  3. Retorna ao passo 3 do fluxo principal

#### 4.5.3 Filtrar/Buscar Trilhas
- **4.5.3a.** O usuário pode filtrar ou buscar trilhas:
  1. O usuário digita termo de busca ou seleciona filtro (categoria)
  2. O sistema atualiza a lista conforme critério
  3. Retorna ao passo 3 do fluxo principal

### 4.6 Pós-condições
- O usuário possui uma trilha pré-definida selecionada
- O progresso foi inicializado (0% concluído)
- O usuário pode visualizar e seguir a trilha

### 4.7 Regras de Negócio
- Um usuário pode ter apenas uma trilha selecionada por vez
- Ao substituir uma trilha, o progresso anterior é perdido
- Apenas trilhas ativas são exibidas para seleção
link miro:https://miro.com/app/board/uXjVJlBSq-M=/?share_link_id=227681969325
---

## 5. Solicitar Trilha Personalizada via LLM

### 5.1 Descrição
Permite que um usuário solicite a criação de uma trilha personalizada baseada em seus requisitos, utilizando um LLM para gerar a trilha automaticamente.

### 5.2 Atores
- **Usuário:** Estudante autenticado
- **Sistema LLM:** Serviço externo de LLM (Gemini/OpenAI)

### 5.3 Pré-condições
- O usuário deve estar autenticado
- O sistema deve ter configuração válida de API do LLM
- O usuário deve fornecer requisitos descritivos

### 5.4 Fluxo Principal
1. O usuário acessa a página "Solicitar Trilha Personalizada"
2. O sistema exibe formulário de solicitação
3. O usuário preenche:
   - Descrição dos objetivos de carreira
   - Área de interesse (opcional)
   - Nível atual (iniciante/intermediário/avançado)
   - Tempo disponível (opcional)
   - Requisitos específicos (texto livre)
4. O usuário submete o formulário
5. O sistema valida os dados (verifica se descrição não está vazia)
6. O sistema cria registro de trilha personalizada com status "PENDENTE"
7. O sistema exibe mensagem: "Sua trilha está sendo gerada. Você será notificado quando estiver pronta."
8. O sistema envia requisição assíncrona ao LLM com:
   - Prompt estruturado contendo requisitos do usuário
   - Instruções para gerar trilha com etapas ordenadas
9. O sistema aguarda resposta do LLM
10. O sistema recebe resposta do LLM (JSON estruturado)
11. O sistema valida a resposta:
    - Verifica estrutura JSON
    - Valida campos obrigatórios (título, descrição, etapas)
    - Verifica número mínimo de etapas (pelo menos 3)
12. O sistema cria a trilha (tipo = "PERSONALIZADA") com os dados do LLM
13. O sistema cria as etapas associadas
14. O sistema atualiza status para "CONCLUIDA"
15. O sistema seleciona automaticamente a trilha para o usuário
16. O sistema notifica o usuário (email ou notificação in-app)
17. O sistema redireciona para visualização da trilha gerada
18. **Fim do caso de uso**

### 5.5 Fluxos Alternativos

#### 5.5.1 Erro na Resposta do LLM
- **5.5.1a.** Se a resposta do LLM for inválida ou incompleta:
  1. O sistema atualiza status para "ERRO"
  2. O sistema registra o erro
  3. O sistema notifica o usuário: "Erro ao gerar trilha. Tente novamente ou entre em contato com suporte"
  4. O usuário pode tentar novamente
  5. Retorna ao passo 2 do fluxo principal

#### 5.5.2 Timeout do LLM
- **5.5.2a.** Se o LLM não responder em tempo hábil:
  1. O sistema atualiza status para "ERRO"
  2. O sistema notifica o usuário
  3. O sistema oferece opção de tentar novamente
  4. Retorna ao passo 2 do fluxo principal

#### 5.5.3 Validação de Requisitos
- **5.5.3a.** Se a descrição estiver vazia ou muito curta:
  1. O sistema exibe erro: "Por favor, forneça uma descrição mais detalhada dos seus objetivos"
  2. Retorna ao passo 3 do fluxo principal

#### 5.5.4 Cancelar Solicitação
- **5.5.4a.** O usuário pode cancelar antes da submissão:
  1. O usuário clica em "Cancelar"
  2. O sistema retorna ao dashboard
  3. **Fim do caso de uso**

### 5.6 Pós-condições
- Uma trilha personalizada foi criada e associada ao usuário
- A trilha foi automaticamente selecionada
- O usuário pode visualizar e seguir a trilha gerada

### 5.7 Regras de Negócio
- O prompt enviado ao LLM deve ser estruturado e incluir contexto do sistema
- A resposta do LLM deve ser em JSON com estrutura: `{titulo, descricao, area, etapas: [{titulo, descricao, ordem}]}`
- Uma trilha personalizada deve ter no mínimo 3 etapas
- O sistema deve validar e sanitizar a resposta do LLM antes de criar a trilha
- Trilhas personalizadas são visíveis apenas para o usuário que as criou

### 5.8 Diagrama de Sequência

```
Usuário          Sistema          LLM Service      Banco de Dados
  │                 │                    │                 │
  │─── Acessa ──────>│                    │                 │
  │                 │                    │                 │
  │<── Form ────────│                    │                 │
  │                 │                    │                 │
  │─── Requisitos ──>│                    │                 │
  │                 │                    │                 │
  │                 │─── Cria Status ────┼────────────────>│
  │                 │                    │                 │
  │<── "Gerando" ───│                    │                 │
  │                 │                    │                 │
  │                 │─── Request ───────>│                 │
  │                 │                    │                 │
  │                 │                    │─── Processa ────│
  │                 │                    │                 │
  │                 │<── Response ───────│                 │
  │                 │                    │                 │
  │                 │─── Valida ─────────│                 │
  │                 │                    │                 │
  │                 │─── Cria Trilha ────┼────────────────>│
  │                 │                    │                 │
  │<── Notificação ─│                    │                 │
  │                 │                    │                 │
```
link miro: https://miro.com/app/board/uXjVJlBcWiY=/?share_link_id=395903703094
---

## 6. Marcar Etapa como Concluída

### 6.1 Descrição
Permite que um usuário marque uma etapa de sua trilha selecionada como concluída, atualizando seu progresso.

### 6.2 Atores
- **Usuário:** Estudante autenticado

### 6.3 Pré-condições
- O usuário deve estar autenticado
- O usuário deve ter uma trilha selecionada
- A etapa deve pertencer à trilha selecionada
- A etapa não deve estar já concluída

### 6.4 Fluxo Principal
1. O usuário acessa a visualização da trilha
2. O sistema exibe a lista de etapas
3. O usuário identifica uma etapa pendente
4. O usuário clica em "Marcar como Concluída" na etapa
5. O sistema solicita confirmação (opcional, pode ser automático)
6. O usuário confirma
7. O sistema valida:
   - Verifica se a etapa pertence à trilha selecionada
   - Verifica se a etapa não está já concluída
8. O sistema adiciona a etapa à lista de etapas concluídas do `ProgressoUsuario`
9. O sistema recalcula a porcentagem de conclusão
10. O sistema atualiza a interface (marca etapa como concluída visualmente)
11. O sistema exibe mensagem de sucesso (opcional)
12. O sistema atualiza a barra de progresso
13. **Fim do caso de uso**

### 6.5 Fluxos Alternativos

#### 6.5.1 Desmarcar Etapa Concluída
- **6.5.1a.** O usuário pode desmarcar uma etapa concluída:
  1. O usuário clica em "Desmarcar" na etapa concluída
  2. O sistema solicita confirmação
  3. O usuário confirma
  4. O sistema remove a etapa da lista de concluídas
  5. O sistema recalcula a porcentagem
  6. Retorna ao passo 10 do fluxo principal

#### 6.5.2 Tentar Marcar Etapa de Outra Trilha
- **6.5.2a.** Se o usuário tentar marcar etapa de outra trilha:
  1. O sistema exibe erro: "Esta etapa não pertence à sua trilha selecionada"
  2. Retorna ao passo 2 do fluxo principal

#### 6.5.3 Marcar Múltiplas Etapas
- **6.5.3a.** O usuário pode marcar múltiplas etapas de uma vez:
  1. O usuário seleciona múltiplas etapas (checkbox)
  2. O usuário clica em "Marcar Selecionadas"
  3. O sistema valida todas as etapas
  4. O sistema marca todas como concluídas
  5. O sistema recalcula progresso
  6. Retorna ao passo 10 do fluxo principal

### 6.6 Pós-condições
- A etapa foi marcada como concluída no progresso do usuário
- A porcentagem de conclusão foi atualizada
- A interface foi atualizada para refletir o novo estado

### 6.7 Regras de Negócio
- Uma etapa só pode ser marcada como concluída se pertencer à trilha selecionada
- A porcentagem é calculada automaticamente: (etapas concluídas / total de etapas) * 100
- Não há ordem obrigatória para concluir etapas (usuário pode pular etapas)
- Quando todas as etapas são concluídas, o sistema pode exibir uma mensagem de parabéns

### 6.8 Diagrama de Sequência

```
Usuário          Sistema          ProgressoUsuario    Banco de Dados
  │                 │                    │                 │
  │─── Visualiza ───>│                    │                 │
  │                 │                    │                 │
  │<── Lista Etapas ─│                    │                 │
  │                 │                    │                 │
  │─── Marcar ──────>│                    │                 │
  │                 │                    │                 │
  │                 │─── Valida ─────────│                 │
  │                 │                    │                 │
  │                 │                    │─── Consulta ────>│
  │                 │                    │<── OK ──────────│
  │                 │                    │                 │
  │                 │─── Adiciona ───────┼────────────────>│
  │                 │                    │                 │
  │                 │─── Recalcula ──────│                 │
  │                 │                    │                 │
  │<── Atualizado ──│                    │                 │
  │                 │                    │                 │
```
link miro: https://miro.com/app/board/uXjVJlAmZAk=/?focusWidget=3458764649795773598
---

