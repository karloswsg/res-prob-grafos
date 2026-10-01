# Marco 3 - Estratégia Algorítmica: Paintball

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 01/10/2026 | Criação do documento: propriedade estrutural, critério, referências do algs4, rastreio manual em fases e análise de complexidade |

---

## Grupo A: Problema I (Paintball | Kattis)

**Link oficial:** <https://open.kattis.com/problems/paintball>

---

## 1. Propriedade Estrutural e Critério

### Propriedade

**Emparelhamento perfeito em grafo bipartido.**

Conforme o Marco 1, cada jogador é desdobrado em duas cópias — **atirador** e **alvo** — e cada par de visão `a–b` gera as arestas `a_atirador → b_alvo` e `b_atirador → a_alvo`.

A organização pedida existe se, e somente se, esse grafo admitir emparelhamento com os `n` atiradores e os `n` alvos todos emparelhados.

### Critério

O emparelhamento é máximo quando não existe **caminho aumentante** — caminho que parte de um atirador livre, termina em um alvo livre e alterna arestas fora e dentro do emparelhamento. Invertendo o papel das arestas ao longo dele, a cardinalidade cresce em uma unidade.

A estratégia adotada busca esses caminhos **em fases**: cada fase calcula as distâncias mínimas por BFS a partir de **todos** os atiradores livres simultaneamente, e em seguida extrai, por DFS, o maior conjunto de caminhos aumentantes **mínimos e disjuntos** disponível. O processo termina quando uma fase não encontra nenhum caminho.

### Obtenção da resposta

| Situação | Saída |
| :--- | :--- |
| cardinalidade final `= n` | para cada jogador `i`, imprimir `mate_atirador[i]` |
| cardinalidade final `< n` | `Impossible` |

Duas condições permitem responder `Impossible` antecipadamente: jogador isolado, e componente conexa de tamanho 1 — detectável pelo `CC` tratado no Marco 2.

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
| `HopcroftKarp.java` | núcleo da estratégia | **adaptada** |
| `graph.py` | lista de adjacência | **reaproveitada** |
| `cc.py` | verificação antecipada de `Impossible` | **opcional** |
| `BipartiteMatching.java` | mesma propriedade, versão mais simples | **não selecionada** |
| `BipartiteX.java` | detecção de bipartição | **descartada** |
| `AssignmentProblem.java` | emparelhamento com custos | **não se aplica** |

### Justificativa da escolha

Ambas as implementações de emparelhamento da biblioteca resolvem o problema e reconhecem a mesma propriedade. A diferença está no custo: `BipartiteMatching` executa `O(V)` buscas, uma por caminho aumentante, resultando em `O(V·E)`; `HopcroftKarp` agrupa caminhos mínimos disjuntos por fase e precisa de `O(√V)` fases, resultando em `O(E√V)`.

Como a solução será escrita em Python, cujo custo por operação é consideravelmente superior ao de Java, a margem de tempo é menor do que a sugerida pelo limite da plataforma. A versão por fases é, portanto, a escolha adequada para este problema.

### Adaptações previstas

**1. Tradução de Java para Python.** Não há equivalente na `algs4-py`; a lógica das fases e da extração de caminhos é preservada.

**2. Descarte do `BipartiteX`.** A referência **detecta** a bipartição antes de emparelhar. Na modelagem adotada a bipartição é **construída** por desdobramento de papéis e já é conhecida — não há o que detectar.

**3. Simplificação de `isResidualGraphEdge` e `isLevelGraphEdge`.** Na referência, os `2n` vértices convivem em um único `Graph`, e essas funções decidem se uma aresta pode ser atravessada e se ela pertence ao grafo de níveis. Na adaptação, atiradores e alvos ocupam **vetores separados** sobre os mesmos índices, de modo que o sentido da travessia é implícito; resta apenas a comparação de níveis.

**4. Desdobramento sem duplicar o grafo.** Mantém-se a lista de adjacência original de `n` vértices e dois vetores de correspondência, em vez de um grafo de `2n` vértices.

**5. Descarte de `inMinVertexCover`.** A referência também calcula a cobertura mínima de vértices, consequência do teorema de König. O problema não a exige.

**6. Critério de perfeição.** `isPerfect()` compara a cardinalidade com o menor lado da bipartição; aqui os dois lados têm tamanho `n`, logo basta `cardinalidade == n`.

**7. Leitura e saída.** Leitura de `n`, `m` e dos `m` pares; impressão de `n` linhas com o alvo de cada jogador, ou de `Impossible`.

### Correspondência de estruturas

| `HopcroftKarp.java` | Adaptação |
| :--- | :--- |
| `mate[]` | `mate_atirador[]` e `mate_alvo[]` |
| `distTo[]` | `dist[]` — nível de cada atirador na fase |
| `marked[]` | implícito em `dist[] != ∞` |
| `cardinality` | contagem de atiradores emparelhados |
| `hasAugmentingPath()` | BFS de fase |
| `isLevelGraphEdge()` | comparação `dist[u] == dist[v] + 1` |
| `isResidualGraphEdge()` | eliminado |
| `inMinVertexCover[]` | eliminado |

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
| `mate_atirador[v]` | alvo em que o jogador `v` atira |
| `mate_alvo[w]` | jogador que atira no alvo `w` |
| `dist[v]` | nível do atirador `v` na fase corrente; `∞` se inalcançável |

Estado inicial: tudo não emparelhado, cardinalidade `0`.

---

### Fase 1

**BFS.** Todos os seis atiradores estão livres, logo todos recebem `dist = 0`.

```text
dist = [0, 0, 0, 0, 0, 0]
```

Como existem alvos livres adjacentes a atiradores de nível 0, os caminhos aumentantes mínimos desta fase têm **comprimento 1** — uma única aresta, de atirador livre para alvo livre.

**DFS — extração dos caminhos disjuntos.**

| Atirador | Primeiro alvo livre | Decisão |
| :-: | :--- | :--- |
| 1 | `2` | emparelha `1 → 2` |
| 2 | `1` | emparelha `2 → 1` |
| 3 | `1` e `2` já tomados nesta fase | sem caminho |
| 4 | `1` e `2` já tomados nesta fase | sem caminho |
| 5 | `6` | emparelha `5 → 6` |
| 6 | `5` | emparelha `6 → 5` |

```text
mate_atirador = [2, 1, –, –, 6, 5]
caminhos na fase: 4        cardinalidade: 4
```

Os atiradores `3` e `4` permanecem livres: ambos só enxergam `1` e `2`, cujos alvos já foram tomados nesta mesma fase por caminhos disjuntos.

---

### Fase 2

**BFS.** Atiradores livres: `3` e `4`, com `dist = 0`. A busca avança: a partir de `3`, o alvo `1` está ocupado pelo atirador `2`, que recebe `dist = 1`; a partir de `4`, o alvo `2` está ocupado pelo atirador `1`, que recebe `dist = 1`.

```text
dist = [1, 1, 0, 0, ∞, ∞]
```

Os atiradores `5` e `6` ficam em `∞`: estão em outra componente, inalcançáveis a partir dos livres. A BFS encontra alvos livres (`3` e `4`) no nível seguinte, de modo que os caminhos mínimos desta fase têm **comprimento 3**.

**DFS — extração dos caminhos disjuntos.**

**Caminho a partir de `3`:**

```text
3 ──> alvo 1  (ocupado por 2, e dist[2] = dist[3] + 1 ✓)
      2 ──> alvo 3  (LIVRE)
```

Inversão: `2` passa a atirar em `3`; `3` assume o alvo `1`.

**Caminho a partir de `4`:**

```text
4 ──> alvo 2  (ocupado por 1, e dist[1] = dist[4] + 1 ✓)
      1 ──> alvo 4  (LIVRE)
```

Inversão: `1` passa a atirar em `4`; `4` assume o alvo `2`.

```text
mate_atirador = [4, 3, 1, 2, 6, 5]
caminhos na fase: 2        cardinalidade: 6
```

Os dois caminhos têm o mesmo comprimento e **não compartilham vértice algum** — por isso foram extraídos na mesma fase.

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

Verificação: os alvos `4, 3, 1, 2, 6, 5` são todos distintos — cada jogador recebe exatamente um disparo. E cada disparo respeita a visão: `1–4` ✓, `2–3` ✓, `3–1` ✓, `4–2` ✓, `5–6` ✓, `6–5` ✓.

### Decisões relevantes do algoritmo

Na Fase 2, o atirador `2` **já estava emparelhado** e ainda assim trocou de alvo. É o que distingue o caminho aumentante de uma busca por vaga livre: ele realoca escolhas anteriores em vez de apenas preencher lacunas.

O vetor `dist[]` cumpre dois papéis: estabelece o nível de cada atirador, restringindo a DFS a arestas que avançam exatamente um nível, e serve como marcação de visita, impedindo reexploração dentro da mesma fase.

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

### Memória — representação do grafo

| Estrutura | Custo |
| :--- | :--- |
| Lista de adjacência | `O(V + E)` |

São `V` listas, uma por jogador — custo pago mesmo sem nenhuma aresta — e cada par de visão é armazenado duas vezes, uma em cada extremidade, totalizando `2E` entradas.

### Memória — auxiliar do algoritmo

| Estrutura | Custo |
| :--- | :--- |
| `mate_atirador[]`, `mate_alvo[]` | `O(V)` |
| `dist[]` | `O(V)` |
| fila da BFS | `O(V)` |
| pilha da DFS | `O(V)` |
| **Total auxiliar** | **`O(V)`** |

Nenhuma estrutura auxiliar cresce com o número de arestas: o algoritmo **percorre** as arestas, mas não armazena nenhuma.

### Distinção

O consumo total é `O(V + E)`, mas a parcela dependente de `E` vem **exclusivamente da representação do grafo**. O algoritmo acrescenta apenas `O(V)`.

A adaptação é ainda mais econômica que a referência, que constrói um grafo com `2n` vértices, enquanto aqui se mantêm `n` vértices e dois vetores de correspondência.
