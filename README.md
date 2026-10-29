# Play Toy — Sistema de cadastro de brinquedos

## Vídeo do projeto

[Assista ao vídeo do projeto](https://drive.google.com/file/d/1E3vKGhETiHkY98fElbTJr3yyNXwD6Ho1/view?usp=sharing)

O Play Toy é um sistema simples para organizar o catálogo e a disponibilidade de uma loja de brinquedos. Ele ajuda a manter os dados dos produtos em um só lugar e permite consultar rapidamente quais itens estão ou não em estoque.

## Objetivo e funcionalidades

A aplicação oferece uma interface web feita com Streamlit e uma versão de terminal em Python. Na interface web é possível:

- cadastrar brinquedos com ID, nome, marca, preço e disponibilidade;
- listar os produtos cadastrados;
- buscar por ID, nome ou marca;
- atualizar dados e disponibilidade;
- remover produtos;
- consultar relatórios de brinquedos por marca e por disponibilidade de estoque.

O cadastro valida IDs e preços não negativos. A versão web persiste os dados no Supabase. A versão de terminal (`Main/Codigo_Python/Play_Toy.py`) mantém os dados apenas na memória durante a execução e não compartilha o banco da versão web.

## Tecnologias

- Python 3.12
- Streamlit para a interface web
- Supabase (PostgreSQL e API) para persistência dos dados da versão web
- Redis 7 para cache da lista de brinquedos
- Docker e Docker Compose para executar a aplicação e o Redis em containers

## Configuração e execução com Docker

### Pré-requisitos

- Docker Desktop ou Docker Engine com Docker Compose;
- um projeto Supabase.

### 1. Preparar o banco Supabase

No painel do Supabase, abra **SQL Editor → New query**, copie o conteúdo de [`Main/supabase/schema.sql`](Main/supabase/schema.sql) e execute-o. O script cria `public.brinquedos`, concede permissões de CRUD e configura uma política RLS pública para a demonstração.

Em **Project Settings → API** (ou **Data API**), copie a URL do projeto e a chave **publishable**. Configure-as no próximo passo. O schema permite acesso anônimo de leitura e escrita: use-o somente para demonstração. Para produção, implemente autenticação e políticas RLS que restrinjam o acesso.

### 2. Configurar variáveis

Na raiz do repositório, crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Edite `.env` e informe as credenciais do projeto:

```dotenv
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_KEY=sua-chave-publishable
```

O Compose configura `REDIS_URL=redis://redis:6379/0` automaticamente. Não publique nem envie o `.env` ao Git.

### 3. Iniciar

Na raiz do projeto, execute:

```bash
docker compose up --build -d
```

Acesse [http://localhost:8501](http://localhost:8501). Para acompanhar os logs ou parar os containers:

```bash
docker compose logs -f app
docker compose down
```

O Redis usa o volume Docker `redis_data`; os dados do catálogo, porém, ficam no Supabase.

## Execução local sem Docker

Requer Python 3.12 ou compatível. Instale as dependências:

```bash
pip install -r Main/requirements.txt
```

Defina `SUPABASE_URL` e `SUPABASE_KEY` no ambiente. Para usar também o cache, inicie um Redis e defina `REDIS_URL` com a URL de conexão. Por exemplo, em uma sessão Bash:

```bash
export SUPABASE_URL="https://seu-projeto.supabase.co"
export SUPABASE_KEY="sua-chave-publishable"
export REDIS_URL="redis://localhost:6379/0"
streamlit run Main/app.py
```

Sem `REDIS_URL` ou se o Redis estiver indisponível, a aplicação continua consultando o Supabase diretamente. Para executar a versão de terminal:

```bash
python Main/Codigo_Python/Play_Toy.py
```

## Integração com Supabase

A aplicação web lê `SUPABASE_URL` e `SUPABASE_KEY` do ambiente ou dos secrets do Streamlit e cria um cliente Supabase. As operações de cadastro, listagem, atualização e remoção usam a tabela `public.brinquedos`, definida em `Main/supabase/schema.sql`. Os dados persistem no PostgreSQL do Supabase entre execuções.

O formato da tabela inclui `id`, `nome`, `marca`, `preco`, `disponibilidade` e `criado_em`. O script SQL habilita RLS, mas sua política concede acesso completo às funções `anon` e `authenticated`; por isso, serve apenas para ambiente de demonstração.

## Uso do Redis

O Redis é usado como cache de leitura na versão Streamlit. A função de listagem consulta a chave `play_toy:brinquedos`; se ela existir, retorna a lista em cache. Em caso de ausência, busca os dados no Supabase e guarda o resultado no Redis por 60 segundos. Depois de cadastrar, atualizar ou remover um item, a aplicação apaga essa chave para que a próxima listagem reflita os dados atuais.

O cache reduz consultas repetidas ao banco e melhora o tempo de resposta da listagem. O Redis foi escolhido por ser um armazenamento em memória rápido, adequado a dados temporários que podem ser reconstruídos a partir do Supabase. Se o Redis não estiver configurado ou ficar indisponível, o sistema trata o cache como opcional e segue usando o banco diretamente. No Compose, o serviço Redis é iniciado junto com a aplicação e conectado pelo hostname `redis`.

## Imagens da aplicação

Este repositório não contém capturas de tela da interface até o momento. As telas disponíveis são **Cadastrar**, **Listar**, **Atualizar**, **Remover**, **Relatórios**, **Buscar** e **Sair**. A versão hospedada pode ser acessada [neste link do Streamlit](https://playtoy-jdxsicqhxvgmps9ztavcpr.streamlit.app).
