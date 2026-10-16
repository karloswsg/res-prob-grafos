# Marco 4 - Implementação Final e Conclusão: Paintball

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 08/10/2026 | Criação do documento: consolidação da solução, módulos reutilizados e modificados, testes executados e evidência do `Accepted` |
| 2.0     | 16/10/2026 | Reescrita após reorientação: a solução passa a ser tradução fiel de `HopcroftKarp.java`, com grafo de `2n` vértices, `isResidualGraphEdge`, `isLevelGraphEdge` e DFS com pilha explícita; acréscimo da seção de detalhes de implementação |

---

## Grupo A: Problema I (Paintball | Kattis)

**Link oficial:** <https://open.kattis.com/problems/paintball>
**Solução:** `T2/src/main.py` · **Linguagem:** Python 3

---

## 1. Solução Consolidada

A solução final está em `src/main.py` e é uma **tradução de `algs4-java/HopcroftKarp.java` para Python**, preservando a estrutura da referência.

| Bloco | Responsabilidade |
| :--- | :--- |
| 1. `Graph` | lista de adjacência, equivalente a `algs4.Graph` |
| 2. `build_bipartite_graph` | desdobra os papéis e monta os `2n` vértices |
| 3. `Bipartition` | informa de que lado está cada vértice |
| 4. `HopcroftKarp` | o algoritmo: laço de fases, BFS, DFS, resíduo e níveis |
| 5. `main` | leitura, execução e saída |

### Estruturas de dados

| Estrutura | Papel |
| :--- | :--- |
| `mate[v]` | vértice emparelhado com `v`; `-1` se livre. Tamanho `2n` |
| `marked[v]` | `v` é alcançável por caminho alternante nesta fase |
| `dist_to[v]` | nível de `v` no grafo de níveis; `INFINITY` se inalcançável |
| `path` | pilha com o caminho aumentante em construção |
| `next_edge[v]` | índice do próximo vizinho de `v` ainda não testado |
| `cardinality` | número de pares no emparelhamento |

---

## 2. Construção do Grafo Bipartido

O grafo da entrada não é bipartido. A bipartição é **construída** pelo desdobramento de papéis, pois cada jogador exerce dois papéis independentes: em quem atira e quem atira nele.

```python
G = Graph(2 * n)
for a, b in pairs:
    if a != b:  G.add_edge(a, n + b)   # a atira em b
    if b != a:  G.add_edge(b, n + a)   # b atira em a
```

| Índice | Significado |
| :--- | :--- |
| `0 .. n-1` | atiradores (lado L) |
| `n .. 2n-1` | alvos (lado R) |

Cada par de visão gera **duas** arestas, porque a visão é mútua. A condição `a != b` impede a aresta `i – (n+i)`, isto é, a restrição de que ninguém atira em si mesmo.

---

## 3. Módulos Reutilizados e Modificados

| Referência | Decisão | Justificativa |
| :--- | :--- | :--- |
| `HopcroftKarp.java` | **traduzida** | núcleo da solução |
| `Graph.java` | **traduzida** | lista de adjacência |
| `BipartiteX.java` | **substituída** | detecta a bipartição por ciclo ímpar; a nossa é construída e já conhecida |
| `BipartiteMatching.java` | não utilizada | mesmo resultado com custo `O(V·E)`, superior ao `O(E√V)` |
| `AssignmentProblem.java` | não utilizada | trata emparelhamento com custos; o problema não tem pesos |

### Tradução de Java para Python

A `algs4-py` **não contém nenhuma implementação de emparelhamento**. Foram verificados os 30 módulos disponíveis: há `cc`, `kosaraju_scc`, `topological`, `dijkstra` e as árvores geradoras mínimas, mas nada de emparelhamento bipartido. As implementações existem apenas em `algs4-java`, o que tornou a tradução necessária.

| Elemento em Java | Equivalente em Python |
| :--- | :--- |
| `Integer.MAX_VALUE` | `float('inf')` |
| `Queue<Integer>` do algs4 | `collections.deque` |
| `Stack<Integer>` do algs4 | lista Python usada como pilha |
| `Iterator<Integer>[] adj` | vetor `next_edge[]` de índices |
| `BipartiteX` | classe `Bipartition` |
| `StdIn` / `StdOut` | `sys.stdin.buffer` / `sys.stdout` |

### Alterações em relação à referência

| # | Alteração | Justificativa |
| :-: | :--- | :--- |
| 1 | tradução de Java para Python | ausência de implementação de emparelhamento na `algs4-py` |
| 2 | `BipartiteX` substituído por `Bipartition` | a referência percorre o grafo procurando ciclo ímpar para decidir se é bipartido; aqui a bipartição é construída no desdobramento, de modo que `color(v)` reduz-se a `v < n` |
| 3 | iterador de Java substituído por `next_edge[]` | Python não possui `Iterator` sobre lista de adjacência; o vetor de índices cumpre o mesmo papel de lembrar em que vizinho cada vértice parou |
| 4 | `inMinVertexCover[]` não implementado | a referência também calcula a cobertura mínima de vértices, consequência do teorema de König; o problema não a exige |
| 5 | `isPerfect()` compara com `n` | a referência compara com `min(V1, V2)`; aqui os dois lados têm o mesmo tamanho |
| 6 | acréscimo de leitura e saída | a referência opera sobre um `Graph` já construído |

**Idioma dos identificadores.** Como as estruturas herdadas da referência já estão em inglês (`Graph`, `mate`, `marked`, `dist_to`, `add_edge`), todo o código, incluindo nomes próprios e comentários, foi padronizado em inglês, evitando mistura de idiomas. A documentação permanece em português.

**A lógica do algoritmo foi preservada integralmente.** O laço de fases, a BFS de níveis, a DFS com pilha explícita, o teste de resíduo e o critério de parada permanecem como na referência.

---

## 4. Detalhes de Implementação

Esta seção registra os pontos do código que não foram detalhados na apresentação.

### 4.1 O teste de resíduo

```python
def _is_residual_graph_edge(self, v, w):
    if self.mate[v] != w and     self.bipartition.color(v):  return True
    if self.mate[v] == w and not self.bipartition.color(v):  return True
    return False
```

É o conceito de **fluxo** dentro do algoritmo. Toda aresta tem capacidade 1; uma aresta emparelhada está **saturada**, e uma não emparelhada tem **resíduo**.

| Lado | Só atravessa aresta | Razão |
| :--- | :--- | :--- |
| atirador (`color = True`) | **não** emparelhada | ainda há resíduo, cabe fluxo |
| alvo (`color = False`) | emparelhada | é o retorno pelo fluxo já enviado |

É esta função que faz o caminho **alternar** entre arestas fora e dentro do emparelhamento. Sem ela, a busca percorreria qualquer aresta e o caminho deixaria de ser alternante.

### 4.2 O grafo de níveis

```python
def _is_level_graph_edge(self, v, w):
    return self.dist_to[w] == self.dist_to[v] + 1 \
           and self._is_residual_graph_edge(v, w)
```

Duas condições simultâneas: a aresta **avança exatamente um nível** e **tem resíduo**. A primeira obriga a DFS a andar apenas para frente, o que garante que os caminhos encontrados sejam os **mínimos** daquela fase.

Sem essa restrição, a DFS poderia encontrar caminhos aumentantes com desvio. O algoritmo ainda funcionaria, mas perderia o limite de `O(√V)` fases e deixaria de ser Hopcroft-Karp.

### 4.3 A BFS mede, não encontra

```python
for v in range(self.V):
    if self.bipartition.color(v) and not self._is_matched(v):
        queue.append(v); self.marked[v] = True; self.dist_to[v] = 0
```

A BFS parte de **todos os atiradores livres simultaneamente**, todos com nível 0. Diferentemente da BFS do T1, que partia de uma única origem.

Ela não encontra caminho aumentante algum. Sua função é dupla: atribuir níveis e responder se **ainda existe** caminho aumentante, o que ocorre quando alcança um alvo livre.

```python
if not self._is_matched(w): found = True
if not found: queue.append(w)
```

Após encontrar o primeiro alvo livre, a BFS deixa de enfileirar: o comprimento mínimo daquela fase já está determinado, e caminhos mais longos não interessam. Quando a BFS devolve falso, o laço de fases termina.

### 4.4 A DFS com pilha explícita

```python
path = [s]
while path:
    v = path[-1]                          # topo, sem retirar
    if next_edge[v] >= len(self.G.adj(v)):
        path.pop(); continue              # RECUA
    w = self.G.adj(v)[next_edge[v]]; next_edge[v] += 1
    if not self._is_level_graph_edge(v, w): continue
    path.append(w)                        # AVANCA
    if not self._is_matched(w):
        while path:                       # caminho completo esta aqui
            x = path.pop(); y = path.pop()
            self.mate[x] = y; self.mate[y] = x
        self.cardinality += 1
```

Toda recursão é uma pilha; a diferença está em quem a mantém. A referência usa **pilha explícita**, e a tradução preserva essa escolha.

A vantagem é que, ao alcançar um alvo livre, o **caminho aumentante completo está contido na variável `path`**, podendo ser exibido. Na versão recursiva, o caminho jamais existe reunido em um único lugar: permanece distribuído entre as chamadas aninhadas.

**O vetor `next_edge[]`.** Com recursão, o `for` guardava automaticamente em que vizinho cada chamada havia parado. Com pilha explícita, essa posição precisa ser registrada manualmente; sem isso, ao retornar ao topo da pilha o algoritmo recomeçaria a lista do início e entraria em laço.

**A inversão do caminho.** O `while path` percorre a pilha **em pares**, porque o caminho alterna atirador e alvo. Cada par de `pop` retira um alvo e o atirador que o precedeu, e o emparelhamento entre eles é firmado. Não existe função separada de inversão: ela é o próprio esvaziamento da pilha.

### 4.5 A saída

```python
output = "\n".join(str(hk.mate[i] - n + 1) for i in range(n))
```

`mate[i]` guarda o **vértice** do alvo, cujo valor é `n + jogador`. Subtrai-se `n` para recuperar o número do jogador, e soma-se `1` porque a entrada numera de `1` a `n` enquanto os vetores usam `0` a `n-1`.

A resposta do problema é, portanto, a **leitura direta do vetor `mate`**. A DFS não produz a resposta: ela preenche o `mate`.

---

## 5. Testes Executados

### Caso positivo

```text
Entrada:        Saída obtida:
2 1             2
1 2             1
```

Dois jogadores que se enxergam. O emparelhamento perfeito existe e é único.

**Verificação:** os alvos `2` e `1` são distintos, logo cada jogador recebe exatamente um disparo. Ambos os disparos respeitam a aresta `1–2`.

### Caso negativo 1: jogador isolado

```text
Entrada:        Saída obtida:
3 1             Impossible
1 2
```

O jogador `3` não aparece em nenhum par, portanto não enxerga ninguém. Sua cópia de atirador não possui aresta alguma.

**Verificação:** a cardinalidade final é `2`, inferior a `n = 3`. O laço de fases encerra quando a BFS não encontra mais caminho aumentante.

### Caso negativo 2: grafo conexo sem solução

```text
Entrada:        Saída obtida:
3 2             Impossible
1 2
2 3
```

Os jogadores `1` e `3` enxergam apenas o `2`. Ambos precisariam atirar nele, mas o alvo `2` admite um único atirador.

**Verificação:** a cardinalidade final é `2`. Este caso é relevante porque o grafo é **conexo** e ainda assim não há solução: a conexidade não determina a existência de emparelhamento perfeito.

### Caso-limite 1: atribuição cíclica

```text
Entrada:        Saída obtida:
3 3             3
2 3             1
1 3             2
1 2
```

Triângulo de visibilidade. A solução obtida é o ciclo `1 → 3 → 2 → 1`.

**Verificação:** os alvos `3, 1, 2` formam uma permutação de `1..3`. Nenhum par atira mutuamente, o que confirma que a solução não exige reciprocidade: o emparelhamento ocorre entre as **cópias** de atirador e de alvo, não entre jogadores.

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

**Verificação:** os alvos `4, 3, 1, 2, 6, 5` formam uma permutação de `1..6`, e cada disparo respeita uma aresta existente. O caso confirma que **desconexão não implica `Impossible`**: cada componente admite internamente uma atribuição completa.

### Verificação aplicada a todos os casos

- a saída é sempre uma permutação de `1..n`, garantindo um disparo recebido por jogador;
- nenhum jogador atira em si mesmo, pois a construção descarta a aresta `i – (n+i)`;
- todo disparo corresponde a um par informado na entrada.

Os casos estão registrados em `dados/casos-de-teste.txt`.

---

## 6. Complexidade

| Aspecto | Custo |
| :--- | :--- |
| Tempo | `O(E√V)`: `O(√V)` fases, cada uma `O(V + E)` |
| Memória do grafo | `O(V + E)`: `V` listas e `2E` entradas |
| Memória auxiliar | `O(V)`: `mate`, `marked`, `dist_to`, `path`, `next_edge`, fila |

Nenhuma estrutura auxiliar cresce com o número de arestas: o algoritmo **percorre** as arestas, mas não armazena nenhuma. A parcela dependente de `E` provém exclusivamente da representação do grafo.

O limite de `O(√V)` fases decorre de o menor caminho aumentante crescer a cada fase: após `√V` fases, os caminhos restantes são longos o bastante para que poucos caibam simultaneamente em um grafo de `V` vértices sem compartilhar vértice.

O enunciado estabelece `2 ≤ N ≤ 1000` e `0 ≤ M ≤ 5000`. Medição local no pior caso dessas restrições: **0,04 s**.

---

## 7. Submissão

Submetido no Kattis em Python 3 e aceito: **`Accepted`, 0,06 s de um limite de 3 s, 29 de 29 casos de teste**. Evidência em `evidencias/accepted.png`.

---

## 8. Conclusão

### Relação com fluxo máximo

O emparelhamento em grafo bipartido é um caso particular de **fluxo máximo com capacidades unitárias**. A rede equivalente acrescenta uma fonte `S` ligada a todos os atiradores e um destino `D` ligado a todos os alvos:

| Aresta | Capacidade | Restrição que impõe |
| :--- | :---: | :--- |
| `S → atirador i` | 1 | o jogador `i` atira uma única vez |
| `atirador i → alvo j` | 1 | o jogador `i` enxerga o jogador `j` |
| `alvo j → D` | 1 | o jogador `j` é atingido uma única vez |

Cada unidade de fluxo percorre `S → i → j → D` e corresponde a uma decisão de disparo. O fluxo máximo iguala a cardinalidade do emparelhamento máximo.

A correspondência é direta no código: o `_is_residual_graph_edge` implementa exatamente a noção de capacidade residual, e o caminho aumentante do emparelhamento é o caminho aumentante do fluxo.

A modelagem por fluxo não foi implementada porque, sendo todas as capacidades unitárias e a rede bipartida, o emparelhamento resolve o problema diretamente, sem a estrutura adicional de fonte, destino e controle de capacidade.

### Coloração e isomorfismo

Nenhum dos dois é pertinente. **Coloração** não se aplica: o problema não exige particionar vértices em classes mutuamente não adjacentes. O grafo construído é bipartido, logo 2-colorível, mas isso é consequência da modelagem e não exigência do enunciado; o grafo de visão original pode conter ciclos ímpares, como no triângulo testado. **Isomorfismo** não se aplica: não há comparação entre estruturas.

### Síntese

A etapa determinante do trabalho foi a modelagem. O enunciado não menciona grafos, e foi necessário reconhecer que cada jogador exerce dois papéis independentes, quem ele atinge e quem o atinge, e que desdobrá-lo em duas cópias converte um grafo comum em um grafo bipartido, sobre o qual a pergunta passa a ser a existência de emparelhamento perfeito.

Estabelecida a modelagem, a implementação decorreu da biblioteca de referência. A principal dificuldade não foi algorítmica, mas de fidelidade: compreender por que cada estrutura da referência existe, de modo que a tradução preservasse a lógica em vez de substituí-la por um atalho equivalente.

A validade da solução repousa sobre uma condição que o enunciado não declara explicitamente: a relação de visão é **simétrica**. É isso que permite gerar as duas arestas `a_atirador – b_alvo` e `b_atirador – a_alvo` a partir de cada par da entrada.
