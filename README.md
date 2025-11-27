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
