# Marco 3 - Estratégia Algorítmica: Paintball

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 01/10/2026 | Criação do documento: propriedade estrutural, critério, referências do algs4, rastreio manual em fases e análise de complexidade |
| 1.1     | 08/10/2026 | Explicitação do ponto de partida das buscas; registro da escolha estrutural em relação à referência; nota sobre atribuições cíclicas e sobre a modelagem equivalente por fluxo máximo |
| 1.2     | 16/10/2026 | Revisão das adaptações: o grafo passa a ser construído com `2n` vértices em um único `Graph`, e as funções `isResidualGraphEdge` e `isLevelGraphEdge` são preservadas em vez de eliminadas; correspondência de estruturas e seção de memória atualizadas |

---

## Grupo A: Problema I (Paintball | Kattis)

**Link oficial:** <https://open.kattis.com/problems/paintball>

---

## 1. Propriedade Estrutural e Critério

### Propriedade

**Emparelhamento perfeito em grafo bipartido.**

Conforme o Marco 1, cada jogador é desdobrado em duas cópias, **atirador** e **alvo**, e cada par de visão `a–b` gera as arestas `a_atirador → b_alvo` e `b_atirador → a_alvo`.

A organização pedida existe se, e somente se, esse grafo admitir emparelhamento com os `n` atiradores e os `n` alvos todos emparelhados.

### Critério

O emparelhamento é máximo quando não existe **caminho aumentante**, isto é, caminho que parte de um atirador livre, termina em um alvo livre e alterna arestas fora e dentro do emparelhamento. Invertendo o papel das arestas ao longo dele, a cardinalidade cresce em uma unidade.

A estratégia adotada busca esses caminhos **em fases**: cada fase calcula as distâncias mínimas por BFS a partir de **todos** os atiradores livres simultaneamente, e em seguida extrai, por DFS, o maior conjunto de caminhos aumentantes **mínimos e disjuntos** disponível. O processo termina quando uma fase não encontra nenhum caminho.

### Obtenção da resposta

| Situação | Saída |
| :--- | :--- |
| cardinalidade final `= n` | para cada jogador `i`, imprimir `mate[i] - n + 1` |
| cardinalidade final `< n` | `Impossible` |

Um jogador isolado permite reconhecer `Impossible` de imediato: sua cópia de atirador não possui aresta alguma e nunca será emparelhada.

---

## 2. Implementações de Referência do algs4

### Levantamento

A `algs4-py` **não possui implementação de emparelhamento**. As disponíveis estão em `algs4-java`:

| Arquivo | Conteúdo |
| :--- | :--- |
| `HopcroftKarp.java` | emparelhamento máximo por fases, `O(E√V)` |
| `BipartiteMatching.java` | emparelhamento máximo por caminho simples, `O(V·E)` |
| `BipartiteX.java` / `Bipartite.java` | detecção de bipartição |
| `AssignmentProblem.java` | emparelhamento com custos |
| `cc.py`, `graph.py` (algs4-py) | componentes conexas e lista de adjacência |

### Seleção

| Referência | Papel | Decisão |
| :--- | :--- | :--- |
| `HopcroftKarp.java` | núcleo da estratégia | **traduzida** |
| `Graph.java` | lista de adjacência | **traduzida** |
| `BipartiteX.java` | detecção de bipartição | **substituída** |
| `BipartiteMatching.java` | mesma propriedade, versão mais simples | **não selecionada** |
| `AssignmentProblem.java` | emparelhamento com custos | **não se aplica** |

### Justificativa da escolha

Ambas as implementações de emparelhamento da biblioteca resolvem o problema e reconhecem a mesma propriedade. A diferença está no custo: `BipartiteMatching` executa `O(V)` buscas, uma por caminho aumentante, resultando em `O(V·E)`. O `HopcroftKarp` agrupa caminhos mínimos disjuntos por fase e precisa de `O(√V)` fases, resultando em `O(E√V)`.

Como a solução será escrita em Python, cujo custo por operação é consideravelmente superior ao de Java, a margem de tempo é menor do que a sugerida pelo limite da plataforma. A versão por fases é, portanto, a escolha adequada para este problema.

### Adaptações previstas

**1. Tradução de Java para Python.** Não há equivalente na `algs4-py`. A estrutura da referência é preservada: grafo com `2n` vértices, laço de fases, BFS de níveis, DFS com pilha explícita e teste de resíduo.

**2. Substituição do `BipartiteX`.** A referência **detecta** a bipartição percorrendo o grafo em busca de ciclo ímpar. Na modelagem adotada a bipartição é **construída** pelo desdobramento de papéis e já é conhecida de antemão, de modo que a verificação de cor reduz-se a comparar o índice do vértice com `n`.

**3. Iterador substituído por vetor de índices.** A referência percorre a lista de adjacência com um `Iterator` por vértice, preservado entre iterações da DFS. Python não dispõe de estrutura equivalente sobre lista; um vetor de índices registra em que vizinho cada vértice parou, cumprindo o mesmo papel.

**4. `inMinVertexCover` não implementado.** A referência calcula também a cobertura mínima de vértices, consequência do teorema de König. O problema não a exige.

**5. Critério de perfeição.** `isPerfect()` compara a cardinalidade com o menor lado da bipartição; aqui os dois lados têm tamanho `n`, logo basta `cardinalidade == n`.

**6. Leitura e saída.** Leitura de `n`, `m` e dos `m` pares; impressão de `n` linhas com o alvo de cada jogador, ou de `Impossible`.

**O que foi preservado.** As funções `isResidualGraphEdge` e `isLevelGraphEdge` são mantidas como na referência. A primeira implementa a noção de capacidade residual: toda aresta tem capacidade 1, e uma aresta emparelhada está saturada. É ela que obriga o caminho a alternar entre arestas fora e dentro do emparelhamento. A segunda restringe a DFS às arestas que avançam exatamente um nível, garantindo que os caminhos encontrados sejam os mínimos da fase. A DFS é mantida com **pilha explícita**, também como na referência, o que torna o caminho aumentante completo visível em uma única variável no momento em que é encontrado.

### Correspondência de estruturas

| `HopcroftKarp.java` | Tradução |
| :--- | :--- |
| `mate[]` | `mate[]`, tamanho `2n` |
| `distTo[]` | `dist_to[]` |
| `marked[]` | `marked[]` |
| `cardinality` | `cardinality` |
| `hasAugmentingPath()` | `_has_augmenting_path()` |
| `isLevelGraphEdge()` | `_is_level_graph_edge()` |
| `isResidualGraphEdge()` | `_is_residual_graph_edge()` |
| `Iterator<Integer>[] adj` | vetor `next_edge[]` |
| `BipartiteX` | classe `Bipartition` |
| `inMinVertexCover[]` | não implementado |

---

## 3. Instância Pequena e Rastreio Manual

Mesma instância do Marco 2:

```text
6 6
1 2    2 3
1 3    2 4
1 4    5 6
```

Lista de adjacência (visão):

```text
1: 2, 3, 4        4: 1, 2
2: 1, 3, 4        5: 6
3: 1, 2           6: 5
```

### Estruturas rastreadas

| Estrutura | Significado |
| :--- | :--- |
| `mate[v]` | vértice emparelhado com `v`; `-1` se livre |
| `dist_to[v]` | nível de `v` na fase corrente; `∞` se inalcançável |
| `path` | pilha com o caminho aumentante em construção |

Estado inicial: tudo não emparelhado, cardinalidade `0`.

---

### Fase 1

**BFS.** Todos os seis atiradores estão livres, logo todos recebem `dist = 0`.

```text
dist_to (atiradores) = [0, 0, 0, 0, 0, 0]
```

Como existem alvos livres adjacentes a atiradores de nível 0, os caminhos aumentantes mínimos desta fase têm **comprimento 1**: uma única aresta, de atirador livre para alvo livre.

**DFS: extração dos caminhos disjuntos.**

| Atirador | Primeiro alvo livre | Decisão |
| :-: | :--- | :--- |
| 1 | `2` | emparelha `1 → 2` |
| 2 | `1` | emparelha `2 → 1` |
| 3 | `1` e `2` já tomados nesta fase | sem caminho |
| 4 | `1` e `2` já tomados nesta fase | sem caminho |
| 5 | `6` | emparelha `5 → 6` |
| 6 | `5` | emparelha `6 → 5` |

```text
mate (atiradores) = [2, 1, –, –, 6, 5]
caminhos na fase: 4        cardinalidade: 4
```

Os atiradores `3` e `4` permanecem livres: ambos só enxergam `1` e `2`, cujos alvos já foram tomados nesta mesma fase por caminhos disjuntos.

---

### Fase 2

**BFS.** Atiradores livres: `3` e `4`, com `dist = 0`. A busca avança: a partir de `3`, o alvo `1` está ocupado pelo atirador `2`, que recebe `dist = 1`; a partir de `4`, o alvo `2` está ocupado pelo atirador `1`, que recebe `dist = 1`.

```text
dist_to (atiradores) = [1, 1, 0, 0, ∞, ∞]
```

Os atiradores `5` e `6` ficam em `∞`, pois estão em outra componente e são inalcançáveis a partir dos livres. A BFS encontra alvos livres (`3` e `4`) no nível seguinte, de modo que os caminhos mínimos desta fase têm **comprimento 3**.

**DFS: extração dos caminhos disjuntos.**

**Caminho a partir de `3`:**

```text
3 ──> alvo 1  (ocupado por 2, e dist_to[2] = dist_to[3] + 1 ✓)
      2 ──> alvo 3  (LIVRE)
```

Inversão: `2` passa a atirar em `3`; `3` assume o alvo `1`.

**Caminho a partir de `4`:**

```text
4 ──> alvo 2  (ocupado por 1, e dist_to[1] = dist_to[4] + 1 ✓)
      1 ──> alvo 4  (LIVRE)
```

Inversão: `1` passa a atirar em `4`; `4` assume o alvo `2`.

```text
mate (atiradores) = [4, 3, 1, 2, 6, 5]
caminhos na fase: 2        cardinalidade: 6
```

Os dois caminhos têm o mesmo comprimento e **não compartilham vértice algum**, e por isso foram extraídos na mesma fase.

---

### Fase 3

**BFS.** Não restam atiradores livres; nenhum caminho aumentante é encontrado. O algoritmo encerra.

### Resultado

```text
4
3
1
2
6
5
```

Verificação: os alvos `4, 3, 1, 2, 6, 5` são todos distintos, logo cada jogador recebe exatamente um disparo. E cada disparo respeita a visão: `1–4` ✓, `2–3` ✓, `3–1` ✓, `4–2` ✓, `5–6` ✓, `6–5` ✓.

### Decisões relevantes do algoritmo

Na Fase 2, o atirador `2` **já estava emparelhado** e ainda assim trocou de alvo. É o que distingue o caminho aumentante de uma busca por vaga livre: ele realoca escolhas anteriores em vez de apenas preencher lacunas.

O vetor `dist_to[]` cumpre dois papéis: estabelece o nível de cada atirador, restringindo a DFS a arestas que avançam exatamente um nível, e serve como marcação de visita, impedindo reexploração dentro da mesma fase.

**Ponto de partida das buscas.** As buscas partem dos vértices da cor `True`, que nesta modelagem são os **atiradores**. A escolha do lado é simétrica e não altera a validade do resultado, pois o problema aceita qualquer atribuição completa, mas altera a ordem em que os caminhos aumentantes são encontrados.

**Atribuições cíclicas.** A solução não exige que os disparos sejam recíprocos. Em um triângulo de visibilidade entre três jogadores, por exemplo, a atribuição `1 → 2 → 3 → 1` é válida: cada jogador atira uma vez e é atingido uma vez, sem que nenhum par atire mutuamente. O emparelhamento ocorre entre as cópias de atirador e de alvo, e não entre jogadores.

A instância exigiu **duas fases**. A versão que busca um caminho por vez teria exigido duas buscas adicionais após o emparelhamento inicial.

---

## 4. Complexidade de Tempo e Memória

### Tempo

| Etapa | Custo |
| :--- | :--- |
| Leitura e construção da lista de adjacência | `O(V + E)` |
| BFS de cada fase | `O(V + E)` |
| DFS de cada fase | `O(V + E)` |
| Número de fases | `O(√V)` |
| **Total** | **`O(E√V)`** |

O limite de `O(√V)` fases decorre de uma propriedade do algoritmo: o comprimento do menor caminho aumentante cresce a cada fase. Após `√V` fases, o emparelhamento corrente já está a no máximo `√V` unidades do máximo, e cada fase restante acrescenta ao menos uma unidade.

### Memória: representação do grafo

| Estrutura | Custo |
| :--- | :--- |
| Lista de adjacência | `O(V + E)` |

São `V` listas, uma por jogador, custo pago mesmo sem nenhuma aresta, e cada par de visão é armazenado duas vezes, uma em cada extremidade, totalizando `2E` entradas.

### Memória: auxiliar do algoritmo

| Estrutura | Custo |
| :--- | :--- |
| `mate[]` | `O(V)` |
| `marked[]`, `dist_to[]` | `O(V)` |
| `next_edge[]` | `O(V)` |
| fila da BFS e pilha `path` da DFS | `O(V)` |
| **Total auxiliar** | **`O(V)`** |

Nenhuma estrutura auxiliar cresce com o número de arestas: o algoritmo **percorre** as arestas, mas não armazena nenhuma.

### Distinção

O consumo total é `O(V + E)`, mas a parcela dependente de `E` vem **exclusivamente da representação do grafo**. O algoritmo acrescenta apenas `O(V)`.

A tradução preserva a estrutura da referência: o grafo possui `2n` vértices, e os vetores auxiliares têm o mesmo tamanho. Nesta notação, `V = 2n` e `E = 2m`.

---

## 5. Relação com Fluxo Máximo

O emparelhamento em grafo bipartido é um caso particular de **fluxo máximo** com capacidades unitárias.

A rede equivalente acrescenta dois vértices que não existem no problema: uma fonte `S` e um destino `D`.

| Aresta | Capacidade | Restrição que impõe |
| :--- | :---: | :--- |
| `S → atirador i` | 1 | o jogador `i` atira uma única vez |
| `atirador i → alvo j` | 1 | o jogador `i` enxerga o jogador `j` |
| `alvo j → D` | 1 | o jogador `j` é atingido uma única vez |

Cada unidade de fluxo percorre o trajeto `S → i → j → D` e corresponde exatamente a uma decisão de disparo. O valor do fluxo máximo é, portanto, igual à cardinalidade do emparelhamento máximo, e a resposta é `Impossible` quando esse valor é inferior a `n`.

O caminho aumentante do emparelhamento corresponde ao caminho aumentante do fluxo, e a busca em fases do Hopcroft-Karp corresponde à estratégia de fases empregada em redes de capacidade unitária.

A modelagem por fluxo não foi implementada: como todas as capacidades são unitárias e a rede é bipartida, o emparelhamento resolve o problema diretamente, sem a estrutura adicional de fonte, destino e capacidades.
