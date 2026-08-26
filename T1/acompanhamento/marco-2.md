# Marco 2 - Representação Computacional: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração                                                                                                                                  |
| :------ | :--------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1.0     | 20/08/2026 | Criação do documento                                                                                                                                      |
| 1.1     | 20/08/2026 | Padronização dos índices em base 0; ajuste da origem das medidas estruturais; inclusão da validação da representação com instância pequena         |
| 1.2     | 26/08/2026 | Ajuste da lista de adjacência e da construção do grafo; adição do grau médio às medidas estruturais; substituição da instância pequena para 3x3 |

## 1. Representação Computacional Escolhida

Para um grafo com 64 vértices fixos e regras de adjacência bem definidas (o "L" do cavalo), três representações clássicas poderiam ser adotadas: **matriz de adjacência**, **lista de adjacência** e **representação implícita**.

* **Matriz de adjacência (64×64):** consumiria 4096 posições, das quais apenas 336 (duas vezes o número de arestas) seriam preenchidas com 1. Como a densidade do grafo é baixa (ρ ≈ 0,083), a matriz seria majoritariamente composta por zeros, desperdiçando memória (espaço O(V²)) sem trazer ganho proporcional. Em compensação, oferece verificação de adjacência e acesso direto em O(1).
* **Lista de adjacência (escolhido):** representa cada vértice com uma lista contendo apenas seus vizinhos reais, sendo construída **uma única vez**, no início da execução, para os 64 vértices. O espaço utilizado é O(V+E) = O(64+168), proporcional ao tamanho real do grafo (esparso), e cada consulta aos vizinhos de um vértice custa O(grau(v)) — no pior caso, apenas 8 elementos (grau máximo), contra os 64 que seriam varridos em cada linha de uma matriz de adjacência.
* **Representação implícita :** Evitaria qualquer estrutura de dados persistida, recalculando os vizinhos de cada casa a cada consulta, a partir dos 8 deslocamentos fixos do cavalo. Essa abordagem iria reprocessar os mesmos vizinhos toda vez que um vértice é revisitado durante uma busca, pois não armazena resultado algum entre chamadas. Como não haverá, neste momento, nenhuma forma de computação dinâmica, essa opção foi descartada: o custo de recomputar repetidamente as mesmas listas de vizinhança se torna desnecessário frente a uma estrutura pré-computada e reutilizável.

**Justificativa da escolha:** A lista de adjacência é a mais adequada para este problema porque evita o desperdício de memória da matriz esparsa, evita o reprocessamento repetido de vizinhos que a representação implícita exigiria na ausência de computação dinâmica, e mantém o custo de iteração proporcional ao grau de cada vértice (no máximo 8), o que é ideal para os algoritmos de busca que serão executados sobre o grafo.

Cada casa é identificada pelo par ordenado `(coluna, linha)`, ambos no intervalo `0..7`, convertido para um índice único `i = linha*8 + coluna` no intervalo `0..63`, usado para indexar o vetor de listas de adjacência `(adj[64])`.

## 2. Leitura da Entrada e Construção do Grafo

### 2.1 Leitura da Entrada

Cada linha da entrada contém duas strings (ex.: `e2 e4`), lidas até o fim do arquivo, pois o problema não informa previamente a quantidade de casos de teste. Cada string é decomposta pela **função converterEntrada**, que transforma a notação de xadrez em coordenadas numéricas:

- **Coluna:** um caractere `'a'`–`'h'`, convertido para um índice numérico `0`–`7` (`coluna - 'a'`).
- **Linha:** um dígito `'1'`–`'8'`, convertido para um índice numérico `0`–`7` (`linha - '1'`).
- O par `(coluna, linha)` é então reduzido ao índice único `i = linha*8 + coluna` (`0..63`), usado para consultar diretamente o vetor de listas de adjacência.

A leitura de cada caso de teste apenas identifica quais dois vértices (origem e destino) serão consultados na BFS — a construção do grafo ocorre **uma única vez**, antes do processamento de qualquer caso de teste.

### 2.2 Construção do Grafo (Lista de Adjacência)

Diferentemente da geração sob demanda, o grafo é **pré-computado integralmente** no início da execução, através das seguintes funções:

**Vetor de deslocamentos:** armazena os 8 movimentos possíveis do cavalo, calculados uma única vez e reutilizados para todos os 64 vértices:

```
deslocamentos = [(1,2), (2,1), (2,-1), (1,-2),
                  (-1,-2), (-2,-1), (-2,1), (-1,2)]
```

**Função calcularVizinhos(coluna, linha):** aplica os 8 deslocamentos à posição `(coluna, linha)`, calculando `(coluna+dc, linha+dl)` para cada `(dc, dl)` do vetor, e valida se `0 ≤ coluna+dc ≤ 7` e `0 ≤ linha+dl ≤ 7`. Retorna a lista de posições válidas (os vizinhos reais daquele vértice).

**Montagem da lista de adjacência:** para cada uma das 64 casas do tabuleiro, `calcularVizinhos` é chamada uma única vez, e o resultado é armazenado em `adj[i]`, onde `i` é o índice do vértice (`i = linha*8 + coluna`). Ao final dessa etapa, `adj` é um vetor de 64 listas, cada uma contendo entre 2 e 8 vizinhos, totalizando 168 arestas (336 entradas, pelo Lema do Aperto de Mãos).

```
para cada linha de 0 a 7:
    para cada coluna de 0 a 7:
        i = linha*8 + coluna
        adj[i] = calcularVizinhos(coluna, linha)
```

**Função BFS(origem, destino):** com o grafo já montado, a busca em largura passa a apenas **consultar** `adj[v]` para expandir cada vértice `v`, sem recalcular vizinhos a cada chamada — o custo de expansão de um vértice cai para O(grau(v)).

## 3. Medidas Estruturais Pertinentes

As medidas abaixo foram obtidas a partir da regra de vizinhança descrita na Seção 2, aplicada às 64 casas do tabuleiro:

| Medida                 | Valor    |
| :--------------------- | :------- |
| **Ordem**        | 64       |
| **Tamanho**      | 168      |
| **Grau mínimo** | 2        |
| **Grau médio**  | 5,25     |
| **Grau máximo** | 8        |
| **Densidade**    | ≈ 0,083 |

## 4. Validação da Representação com a Instância Pequena

Instância adotada: **tabuleiro 3×3**, a mesma definida no Marco 1 (Seção 3), com as 9 casas numeradas sequencialmente de `0` a `8`, linha a linha:

```
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
```

**Critérios verificados:**

1. **Simetria** — o movimento é reversível, logo `8 ∈ vizinhos(1)` implica `1 ∈ vizinhos(8)`. Confirmado para todos os pares da tabela.
2. **Lema do Aperto de Mãos** — a soma dos graus das 9 casas é `2×8 + 0 = 16`, e `16 / 2 = 8`, coincidindo com a contagem direta de arestas.
3. **Vértice de grau 0** — a casa central (`4`) não possui nenhum vizinho válido: os 8 deslocamentos aplicados a partir dela caem todos fora dos limites `0..2`. Isso resulta em `adj[4]` sendo uma lista **vazia**, o que a representação por lista de adjacência acomoda naturalmente (ao contrário da representação implícita, que recalcularia essa lista vazia a cada consulta sem nunca sinalizar previamente a ausência de vizinhos).
4. **Desconexão** — como o vértice `4` não se liga a nenhum outro, o grafo fica dividido em duas componentes: `{0,1,2,3,5,6,7,8}` (conexa entre si) e `{4}` (isolada). A BFS a partir de `4` (ou tendo `4` como destino a partir de qualquer outro vértice) deve encerrar sem encontrar caminho — este é o caso de teste que valida o tratamento de "sem caminho" na BFS.
5. **Efeito da borda** — mesmo os vértices de canto do 3×3 (ex.: `0`, `2`, `6`, `8`) têm grau 2, e não grau menor, porque no 3×3 todas as casas restantes estão igualmente próximas das bordas; o efeito de borda mais acentuado só se manifesta no 8×8.

**Medidas do 3×3:**

| Medida       | Valor                     |
| :----------- | :------------------------ |
| Ordem        | 9                         |
| Tamanho      | 8                         |
| Grau mínimo | 0                         |
| Grau médio  | 1,78                      |
| Grau máximo | 2                         |
| Densidade    | ≈ 0,222                  |
| Conexidade   | Desconexa (2 componentes) |

Diferentemente do 8×8 (conexo) e do que se poderia esperar por analogia direta, o 3×3 é **desconexo**, justamente por ser pequeno demais para acomodar o "L" do cavalo a partir do centro. Essa é uma propriedade que só aparece em tabuleiros muito reduzidos, e serve para validar que a implementação da lista de adjacência representa corretamente também vértices sem nenhum vizinho, sem tratamento especial: `adj[4]` é simplesmente uma lista vazia, consultada normalmente pela BFS.

**Consulta manual**— entrada `6 8` (mesmo caso do Marco 1, Seção 3):

```
vizinhos(6) = { 1, 5 }        -> 8 ausente: resposta > 1
vizinhos(1) = { 6, 8 }        -> 8 presente: 6 -> 1 -> 8
```

Caminho de comprimento 2, coincidindo com o resultado esperado de **2 movimentos**.

**Consulta manual** — entrada `0 4` (caso de desconexão):

```
vizinhos(0) = { 5, 7 }
vizinhos(5) = { 0, 6 }
vizinhos(7) = { 0, 2 }
vizinhos(6) = { 1, 5 }
vizinhos(2) = { 3, 7 }
vizinhos(1) = { 6, 8 }
vizinhos(3) = { 2, 8 }
vizinhos(8) = { 1, 3 }
```

A BFS a partir de `0` visita todos os 8 vértices da componente `{0,1,2,3,5,6,7,8}` e nunca alcança `4`, cujo `adj[4]` está vazio — confirmando que a lista de adjacência representa corretamente a ausência de caminho, sem exigir nenhum tratamento adicional na BFS além de verificar se o destino foi marcado como visitado ao final da busca.
