# Todo o sistema de uma loja de brinquedo feito em python
 O projeto é um gerenciador de estoque de uma loja de brinquedos infatis, que procura vender a um publico infanto juvenil.Tem como principais funções para o funcionamento do sistema: 
- Cadastrar Brinquedos
- Listar Brinquedos cadastrados
- Atualizar informações sobre brinquedo
- Deletar brinquedos
- Gerar relatorios expondo os brinquedos
- Buscar brinquedo
### Dados do Brinquedo
| Nome da Estrutura | Tipo | Função |
|-|-|-|
| `ID` | INT |  Identificador unico |
| `nome` | STR |Armazenar nome do produto|
| `marca` |STR | De onde vem o produto |
| `preco` |FLOAT | Demarcar valor do produto |
| `status` |STR |Identificar se tem estoque do produto |
### Exemplo de uso

| ID | Nome | Marca | Preco | status |
|-|-|-|-|-|
| 100 | Boneca Baby Alive | Hasbro| 100.44 | Brinquedo com estoque |
| 101 | Slime Puxa e Estica | Amoeba | 10.95 | Brinquedo com estoque|
| 102 | Carro de brinquedo| Hotwheels | 19.99 | Brinquedo sem estoque |

## Tecnologias Utilizadas
Para uma vizualização melhor nosso cliente tem como opção tanto a versão pelo navegador, que utiliza da biblioteca Python Streamlit , quanto a via terminal.
### Telas da Versão de Navegador
- Cadastrar
- Listar
- Atualizar
- Remover
- Relatorios
- Buscar
- Sair
<p>Cada uma delas seguindo a mesma logica das funções principais do sistema, podendo ser navegada pelo menu a esquerda.
</p>
Para acessar a versão de navegador <a href="https://playtoy-jdxsicqhxvgmps9ztavcpr.streamlit.app"> clique aqui</a>

## Banco de dados e execução com Docker

A versão Streamlit salva os brinquedos no Supabase e usa Redis como cache de leitura (60 segundos). A versão de terminal em `Main/Codigo_Python/Play_Toy.py` continua guardando os dados apenas enquanto o processo está aberto. O `compose.yaml` inicia o Streamlit e um Redis local, com volume persistente para os dados do Redis.

### Criar e configurar o banco Supabase

1. Acesse o projeto Supabase correspondente à `SUPABASE_URL` e abra **SQL Editor → New query**.
2. Abra [`querys.sql`](querys.sql), copie o conteúdo inteiro para a consulta e clique em **Run**. Isso cria a tabela `public.brinquedos`, aplica as permissões necessárias ao app e insere exemplos.
3. Em **Project Settings → API** (ou **Data API**, dependendo da interface), copie a **Project URL** e a chave **publishable**. Use esses valores como `SUPABASE_URL` e `SUPABASE_KEY` no `.env` local. A chave publishable é destinada ao cliente; a política do SQL permite acesso anônimo de leitura e escrita para demonstração. Para dados reais, configure autenticação e políticas RLS mais restritas.

### Subir o container

1. Instale Docker Desktop ou Docker Engine com o plugin Docker Compose.
2. Na raiz do projeto, crie `.env` copiando `.env.example` e substitua os valores pelas credenciais do seu projeto Supabase. Não envie o `.env` ao Git.
3. Execute `docker compose up --build -d`.
4. Abra `http://localhost:8501` no navegador. Para acompanhar a aplicação, execute `docker compose logs -f app`; para desligar os serviços, `docker compose down`. O Redis mantém seus dados no volume `redis_data`.

O Compose define `REDIS_URL=redis://redis:6379/0` para a aplicação. O hostname `redis` é resolvido dentro da rede Docker; não é necessário fornecer uma URL externa do Redis para esta configuração local.

Para rodar sem Docker, instale com `pip install -r Main/requirements.txt`, configure as variáveis de ambiente (incluindo `REDIS_URL`) e execute `streamlit run Main/app.py`. Não coloque chaves reais no repositório.
