# Marco 2 - Representação Computacional: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :------------------------- |
| 1.0     | 20/08/2026 | Criação do documento     |
| 1.1     | 20/08/2026 | Padronização dos índices em base 0; ajuste da origem das medidas estruturais; inclusão da validação da representação com instância pequena |

## 1. Representação Computacional Escolhida

Para um grafo com 64 vértices fixos e regras de adjacência bem definidas (o "L" do cavalo), três representações clássicas poderiam ser adotadas: **matriz de adjacência**, **lista de adjacência** e **representação implícita**.

* **Matriz de adjacência (64×64):** consumiria 4096 posições, das quais apenas 336 (duas vezes o número de arestas) seriam preenchidas com 1. Como a densidade do grafo é baixa, a matriz seria majoritariamente composta por zeros, desperdiçando memória sem trazer ganho algum.
* **Lista de adjacência:** representaria cada vértice com um vetor contendo apenas seus vizinhos reais, sendo mais eficiente em memória que a matriz. É uma opção válida, mas exige a etapa extra de pré-computar e armazenar as listas para os 64 vértices.
* **Representação implícita (escolhida):** como as regras de movimento do cavalo são fixas e idênticas para qualquer casa do tabuleiro, os vizinhos de um vértice `(coluna, linha)` podem ser calculados **sob demanda**, aplicando os 8 deslocamentos possíveis `(±1, ±2)` e `(±2, ±1)` e descartando os que caem fora dos limites do tabuleiro.

**Justificativa da escolha:** a representação implícita é a mais adequada para este problema porque evita gasto de memória com uma matriz esparsa, elimina a etapa de pré-processamento de listas de adjacência, já que os vizinhos são triviais de calcular a partir de uma fórmula fixa, sendo a abordagem natural quando o grafo é gerado por uma regra determinística (o padrão de salto do cavalo), em vez de por uma lista arbitrária de arestas fornecida na entrada.

Cada casa é identificada pelo **par ordenado** `(coluna, linha)`, ambos no intervalo `0..7`. Não é necessário mapear as casas para um índice único, pois nenhuma estrutura indexada é mantida em memória.

## 2. Leitura da Entrada e Construção do Grafo

### 2.1 Leitura da Entrada

Cada linha da entrada contém duas strings (ex.: `e2 e4`), lidas até o fim do arquivo, pois o problema não informa previamente a quantidade de casos de teste. Cada string é decomposta em:

* **Coluna:** um caractere `'a'`–`'h'`, convertido para um índice numérico `0`–`7` (`coluna - 'a'`).
* **Linha:** um dígito `'1'`–`'8'`, convertido para um índice numérico `0`–`7` (`linha - '1'`).

A leitura **não constrói o grafo**: ela apenas identifica quais duas casas serão consultadas.

### 2.2 Construção do Grafo (Geração de Vizinhos)

A função de vizinhança `vizinhos(coluna, linha)` aplica os 8 deslocamentos possíveis do cavalo:

```
deslocamentos = [(1,2), (2,1), (2,-1), (1,-2),
                  (-1,-2), (-2,-1), (-2,1), (-1,2)]
```

Para cada deslocamento `(dc, dl)`, calcula-se a nova posição `(coluna+dc, linha+dl)` e valida-se se `0 ≤ coluna+dc ≤ 7` e `0 ≤ linha+dl ≤ 7`. Somente posições válidas são retornadas como vizinhas. Essa função é chamada a cada expansão de vértice durante a BFS, construindo o grafo "sob demanda" e não como uma estrutura persistida em memória.

O descarte das posições fora dos limites é o que reduz o grau das casas de borda: dos 8 deslocamentos, apenas parte permanece válida próximo às extremidades.

## 3. Medidas Estruturais Pertinentes

As medidas abaixo foram obtidas a partir da regra de vizinhança descrita na Seção 2, aplicada às 64 casas do tabuleiro:

| Medida                                | Valor                                      |
| :------------------------------------ | :----------------------------------------- |
| **Ordem**                       | 64                                         |
| **Tamanho**                     | 168                                        |
| **Grau mínimo**                | 2                                          |
| **Grau máximo**                | 8                                          |
| **Densidade** (2·E / V·(V-1)) | ≈ 0,083                                   |
| **Conectividade**               | Conexo                                     |
| **Bipartição**                | Alternância entre casas claras e escuras  |
| **Diâmetro**                  | 6                                          |

O tamanho decorre da soma dos graus: `336 / 2 = 168`, pelo Lema do Aperto de Mãos.

## 4. Validação da Representação com a Instância Pequena

Instância adotada: **tabuleiro 5×5**, colunas `a`–`e` e linhas `1`–`5`. É o menor tabuleiro em que os 8 deslocamentos do cavalo permanecem todos válidos a partir da casa central (`c3`), permitindo verificar tanto o grau máximo quanto o efeito das bordas.

A regra de vizinhança **não depende do tamanho do tabuleiro**: a mesma função vale no 5×5 e no 8×8, alterando-se apenas o teste de limite. A validação é feita manualmente, conferindo se os vizinhos gerados correspondem ao grafo esperado.

**Vizinhos gerados (recorte):**

| Casa | Grau | Vizinhos |
| :--- | :---: | :--- |
| `a1` | 2 | `b3`, `c2` |
| `b1` | 3 | `a3`, `c3`, `d2` |
| `d2` | 4 | `b1`, `b3`, `c4`, `e4` |
| `c3` | 8 | `a2`, `a4`, `b1`, `b5`, `d1`, `d5`, `e2`, `e4` |

**Critérios verificados:**

1. **Simetria** — o movimento é reversível, logo `c3 ∈ vizinhos(b1)` implica `b1 ∈ vizinhos(c3)`. Confirmado.
2. **Lema do Aperto de Mãos** — a soma dos graus das 25 casas é 96, e `96 / 2 = 48`, coincidindo com a contagem direta de arestas.
3. **Limite superior do grau** — nenhuma casa ultrapassa 8 vizinhos, pois o cavalo dispõe de exatamente 8 deslocamentos. Apenas `c3` atinge 8.
4. **Efeito da borda** — as casas de canto têm grau 2: 6 dos 8 deslocamentos caem fora do tabuleiro. Comportamento idêntico aos cantos do 8×8.
5. **Conexidade** — a partir de qualquer casa é possível alcançar todas as demais.

**Medidas do 5×5:**

| Medida | Valor |
| :--- | :--- |
| Ordem | 25 |
| Tamanho | 48 |
| Densidade | 0,160 |
| Diâmetro | 4 |

A densidade do 5×5 é aproximadamente o dobro da do 8×8. O número de arestas cresce de forma quase linear com a quantidade de casas, enquanto o de pares possíveis cresce com o quadrado — portanto, quanto maior o tabuleiro, mais esparso o grafo, o que reforça a decisão de não usar matriz.

**Consulta rastreada à mão** — entrada `b1 b3`:

```
vizinhos(b1) = { a3, c3, d2 }        -> b3 ausente: resposta > 1
vizinhos(d2) = { b1, b3, c4, e4 }    -> b3 presente: b1 -> d2 -> b3
```

Caminho de comprimento 2, correspondendo a `To get from b1 to b3 takes 2 knight moves.`
