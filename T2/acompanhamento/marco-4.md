# Marco 4 - Implementação Final e Conclusão: Paintball

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 08/10/2026 | Criação do documento: consolidação da solução, módulos reutilizados e modificados, testes executados e evidência do `Accepted` |

---

## Grupo A: Problema I (Paintball | Kattis)

**Link oficial:** <https://open.kattis.com/problems/paintball>
**Solução:** `T2/src/main.py` · **Linguagem:** Python 3

---

## 1. Solução Consolidada

A solução final está em `src/main.py` e implementa o **Hopcroft-Karp** adaptado de `algs4-java/HopcroftKarp.java`, conforme selecionado no Marco 3.

| Trecho | Responsabilidade |
| :--- | :--- |
| `class HopcroftKarp` | emparelhamento máximo por fases |
| `__init__` | inicializa os vetores e executa o laço de fases |
| `_has_augmenting_path` | BFS de fase: calcula os níveis e indica se há caminho aumentante |
| `_dfs` | DFS restrita ao grafo de níveis: colhe um caminho aumentante mínimo |
| `is_perfect` | verifica se a cardinalidade atingiu `n` |
| `main` | leitura, construção da lista de adjacência e saída formatada |

| Estrutura | Papel |
| :--- | :--- |
| `adj[v]` | lista de adjacência da relação de visão |
| `mate_shooter[v]` | alvo em que o jogador `v` atira; é a saída do problema |
| `mate_target[w]` | jogador que atira no alvo `w`; permite continuar o caminho alternado |
| `dist[v]` | nível do atirador `v` na fase corrente; `INF` se inalcançável |
| `cardinality` | número de atiradores emparelhados |

Os vetores `mate_shooter` e `mate_target` são espelhos: `mate_shooter[3] == 1` equivale a `mate_target[1] == 3`. Ambos são mantidos porque cada um responde, em tempo constante, uma pergunta distinta. O primeiro produz a saída; o segundo é consultado pela busca ao alcançar um alvo já ocupado.

---

## 2. Tradução de Java para Python

Esta é a adaptação mais extensa e decorre de uma constatação registrada no Marco 3: **a biblioteca `algs4-py` não contém nenhuma implementação de emparelhamento**. Foram verificados os 30 módulos disponíveis; há `cc`, `kosaraju_scc`, `topological`, `dijkstra` e as árvores geradoras mínimas, mas nada de emparelhamento bipartido. As implementações existem apenas em `algs4-java`.

A transposição preservou integralmente a lógica do algoritmo (fases, níveis, caminhos aumentantes, critério de parada) e alterou apenas o que depende da linguagem.

| Elemento em Java | Equivalente em Python | Natureza |
| :--- | :--- | :--- |
| `Integer.MAX_VALUE` | `float('inf')` | marcador de vértice inalcançável; Python não possui constante análoga |
| `Queue<Integer>` do algs4 | `collections.deque` | fila com remoção em tempo constante no início |
| `boolean[] marked` | implícito em `dist[v] == INF` | o vetor de níveis cumpre também a marcação de visita |
| `int[] mate` de tamanho `2n` | `mate_shooter[]` e `mate_target[]`, de tamanho `n` | separação dos papéis |
| `Graph G` com `2n` vértices | `adj` com `n` vértices | bipartição implícita na estrutura |
| `StdIn` / `StdOut` | `sys.stdin.buffer` / `sys.stdout` | leitura e escrita em bloco |

**Recursão.** O `_dfs` é recursivo, como na referência. A profundidade é limitada pelo comprimento do caminho aumentante da fase, que no Hopcroft-Karp é `O(√V)`. Com `n ≤ 1000`, cerca de 32 níveis.

**Entrada e saída.** A leitura é feita em bloco com `sys.stdin.buffer.read()`, adequada ao formato do problema, que informa previamente a quantidade `m` de pares. A saída é montada em uma única string.

**Índices.** A entrada numera os jogadores de `1` a `n`; os vetores usam `0` a `n-1`. A conversão ocorre na leitura e é desfeita na saída.

---

## 3. Módulos Reutilizados e Modificados

| Referência | Decisão | Justificativa |
| :--- | :--- | :--- |
| `HopcroftKarp.java` | **adaptada** | núcleo da solução; traduzida para Python |
| `graph.py` (algs4-py) | **reutilizada** | lista de adjacência, adotada como lista de listas nativa |
| `BipartiteX.java` | descartada | detecta a bipartição; a desta modelagem é construída por desdobramento e já é conhecida |
| `BipartiteMatching.java` | descartada | mesmo resultado com custo `O(V·E)`, superior ao `O(E√V)` |
| `AssignmentProblem.java` | descartada | trata emparelhamento com custos; o problema não possui pesos |
| `cc.py` (algs4-py) | descartada | a verificação antecipada de `Impossible` mostrou-se desnecessária: o próprio algoritmo retorna cardinalidade inferior a `n` nesses casos |

### Alterações em relação ao `HopcroftKarp.java`

| # | Alteração | Justificativa |
| :-: | :--- | :--- |
| 1 | tradução de Java para Python | ausência de implementação de emparelhamento na `algs4-py` |
| 2 | `mate[]` de tamanho `2n` para dois vetores de tamanho `n` | os papéis de atirador e alvo são independentes; separá-los torna o sentido da travessia implícito |
| 3 | `isResidualGraphEdge()` eliminado | com os papéis em vetores distintos, o sentido não precisa ser decidido em tempo de execução |
| 4 | `isLevelGraphEdge()` reduzido à comparação `dist[u] == dist[v] + 1` | a verificação de nível torna-se uma comparação direta |
| 5 | `BipartiteX` eliminado | a bipartição é construída, não detectada |
| 6 | `inMinVertexCover[]` eliminado | a referência calcula a cobertura mínima de vértices, consequência do teorema de König; o problema não a exige |
| 7 | `isPerfect()` simplificado para `cardinality == n` | os dois lados da bipartição têm o mesmo tamanho |
| 8 | acréscimo de leitura e saída no formato do problema | a referência opera sobre um `Graph` já construído |

**Nenhuma lógica foi acrescentada ao algoritmo.** As alterações são traduções, simplificações ou remoções: a referência é mais geral do que o problema exige, e as partes não utilizadas foram descartadas.

**Ponto de partida das buscas.** A referência inicia pelos alvos livres, pois o `BipartiteX` atribui a cor correspondente àquela partição. Esta adaptação parte dos atiradores livres. A escolha é simétrica e não altera a validade do resultado, pois o problema aceita qualquer atribuição completa, mas altera qual das soluções válidas é produzida.

---

## 4. Testes Executados

### Caso positivo

```text
Entrada:        Saída obtida:
2 1             2
1 2             1
```

Dois jogadores que se enxergam mutuamente. O emparelhamento perfeito existe e é único: cada um atira no outro.

**Verificação:** os alvos `2` e `1` são distintos, logo cada jogador recebe exatamente um disparo. O disparo `1 → 2` respeita a aresta `1–2`, e o disparo `2 → 1` respeita a mesma aresta no sentido inverso.

### Caso negativo 1: vértice isolado

```text
Entrada:        Saída obtida:
3 1             Impossible
1 2
```

O jogador `3` não aparece em nenhum par da entrada, portanto não enxerga ninguém. Sua cópia de atirador não possui aresta alguma e jamais pode ser emparelhada.

**Verificação:** a cardinalidade final é `2`, inferior a `n = 3`. O algoritmo encerra quando uma fase não encontra caminho aumentante, e o `is_perfect` retorna falso.

### Caso negativo 2: grafo conexo sem solução

```text
Entrada:        Saída obtida:
3 2             Impossible
1 2
2 3
```

Os jogadores `1` e `3` enxergam apenas o `2`. Ambos precisariam atirar nele, mas o alvo `2` admite um único atirador.

**Verificação:** a cardinalidade final é `2`. Este caso é relevante porque o grafo é **conexo** e ainda assim não há solução, confirmando que a conexidade não determina a existência de emparelhamento perfeito.

### Caso-limite 1: atribuição cíclica

```text
Entrada:        Saída obtida:
3 3             3
2 3             1
1 3             2
1 2
```

Triângulo de visibilidade. A solução obtida é o ciclo `1 → 3 → 2 → 1`.

**Verificação:** os alvos `3, 1, 2` formam uma permutação de `1..3`, logo cada jogador é atingido exatamente uma vez. Nenhum par atira mutuamente, o que confirma que a solução não exige reciprocidade: o emparelhamento ocorre entre as cópias de atirador e de alvo, não entre jogadores.

### Caso-limite 2: grafo desconexo com solução

```text
Entrada:        Saída obtida:
6 6             4
1 2             3
1 3             1
1 4             2
2 3             6
2 4             5
5 6
```

Duas componentes conexas: `{1,2,3,4}` e `{5,6}`.

**Verificação:** os alvos `4, 3, 1, 2, 6, 5` formam uma permutação de `1..6`. Cada disparo respeita uma aresta existente: `1–4`, `2–3`, `3–1`, `4–2`, `5–6` e `6–5`. O caso confirma que **desconexão não implica `Impossible`**: cada componente admite, internamente, uma atribuição completa.

### Verificações aplicadas a todos os casos

- a saída é sempre uma permutação de `1..n`, garantindo que cada jogador seja atingido exatamente uma vez;
- nenhum jogador atira em si mesmo, pois a lista de adjacência não contém laços;
- todo disparo corresponde a um par informado na entrada.

Os casos estão registrados em `dados/casos-de-teste.txt`.

---

## 5. Complexidade

| Aspecto | Custo |
| :--- | :--- |
| Tempo | `O(E√V)`: `O(√V)` fases, cada uma `O(V + E)` |
| Memória do grafo | `O(V + E)`: `V` listas e `2E` entradas |
| Memória auxiliar | `O(V)`: `mate_shooter`, `mate_target`, `dist`, fila e pilha |

Nenhuma estrutura auxiliar cresce com o número de arestas: o algoritmo percorre as arestas, mas não armazena nenhuma. A parcela dependente de `E` provém exclusivamente da representação do grafo.

O limite de `O(√V)` fases decorre de o menor caminho aumentante crescer a cada fase: após `√V` fases, os caminhos restantes são longos o bastante para que poucos caibam simultaneamente em um grafo de `V` vértices.

O enunciado estabelece `2 ≤ N ≤ 1000` e `0 ≤ M ≤ 5000`, de modo que o grafo é pequeno e o tempo medido confirma folga ampla.

---

## 6. Submissão

Submetido no Kattis em Python 3 e aceito: **`Accepted`, 0,06 s de um limite de 3 s, 29 de 29 casos de teste** (submissão 20635412). Evidência em `evidencias/accepted.png`.

---

## 7. Conclusão

### Fluxo máximo

O emparelhamento em grafo bipartido é um caso particular de fluxo máximo com capacidades unitárias. A rede equivalente acrescenta uma fonte `S` ligada a todos os atiradores e um destino `D` ligado a todos os alvos, com capacidade `1` em cada aresta:

| Aresta | Restrição que impõe |
| :--- | :--- |
| `S → atirador i` | o jogador `i` atira uma única vez |
| `alvo j → D` | o jogador `j` é atingido uma única vez |

Cada unidade de fluxo percorre `S → i → j → D` e corresponde a uma decisão de disparo. O valor do fluxo máximo iguala a cardinalidade do emparelhamento máximo.

A modelagem por fluxo não foi implementada: sendo todas as capacidades unitárias e a rede bipartida, o emparelhamento resolve o problema diretamente.

### Coloração e isomorfismo

Nenhum dos dois é pertinente.

**Coloração** não se aplica: o problema não exige particionar vértices em classes mutuamente não adjacentes. O grafo construído é bipartido, logo 2-colorível, mas isso é consequência da modelagem adotada e não exigência do enunciado. O grafo de visão original pode conter ciclos ímpares, como no triângulo testado acima.

**Isomorfismo** não se aplica: não há comparação entre estruturas. O problema opera sobre um único grafo.

### Síntese

A etapa determinante do trabalho foi a modelagem, não o algoritmo. O enunciado não menciona grafos, e foi necessário reconhecer que cada jogador exerce dois papéis independentes, quem ele atinge e quem o atinge, e que desdobrá-lo em duas cópias converte um grafo comum em um grafo bipartido, sobre o qual a pergunta vira a existência de emparelhamento perfeito.

Estabelecida a modelagem, o restante decorreu da biblioteca de referência. A adaptação consistiu majoritariamente em remover o que a referência oferece a mais e em traduzir o que restou para Python.

A validade da solução repousa sobre uma condição que o enunciado não declara: a relação de visão é simétrica. É isso que permite gerar as duas arestas `a_atirador → b_alvo` e `b_atirador → a_alvo` a partir de cada par da entrada.
