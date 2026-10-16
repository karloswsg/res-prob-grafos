# Paintball (Kattis): Emparelhamento Perfeito com Hopcroft-Karp

**Grupo A · Problema I** · [open.kattis.com/problems/paintball](https://open.kattis.com/problems/paintball)

| Integrante | Matrícula |
| :--- | :--- |
| Karlos Eduardo Sousa Pinto | 2320262 |
| Maria Eduarda Coutinho Angelim | 2324319 |

**Linguagem:** Python 3 · **Execução:** `python src/main.py < dados/casos-de-teste.txt`
**Resultado:** `Accepted`, 0,10 s de um limite de 3 s, 29/29 casos (submissão 20671709). Evidência em [`evidencias/accepted.png`](evidencias/accepted.png).

---

## Problema

`N` jogadores (2 ≤ N ≤ 1000) e `M` pares de visão mútua (0 ≤ M ≤ 5000). Cada jogador tem uma bala, só atira em quem enxerga e deve ser atingido exatamente uma vez. Imprimir o alvo de cada jogador, ou `Impossible`.

---

## Modelagem

O grafo da entrada não é bipartido. Cada jogador exerce **dois papéis independentes**, quem ele atinge e quem o atinge, e é desdobrado em duas cópias:

```text
atirador i  ->  vertice  i        (lado L)
alvo     j  ->  vertice  n + j    (lado R)
```

Cada par de visão gera duas arestas, pois a visão é simétrica. Nunca existe a aresta `i` para `n+i`: ninguém atira em si mesmo. O grafo resultante tem `2n` vértices e `2m` arestas.

**Propriedade estrutural:** existe resposta se, e somente se, esse grafo admitir **emparelhamento perfeito**.

---

## Algoritmo

**Hopcroft-Karp**, emparelhamento máximo por fases, **`O(E√V)`**.

O emparelhamento é máximo quando não existe **caminho aumentante**, isto é, caminho que parte de um atirador livre, alterna arestas fora e dentro do emparelhamento e termina em um alvo livre. Invertendo-o, a cardinalidade cresce em uma unidade.

Cada fase executa uma **BFS**, que atribui níveis a partir de todos os atiradores livres, e em seguida uma **DFS** restrita às arestas que avançam exatamente um nível, extraindo vários caminhos mínimos e disjuntos. O processo repete até que uma fase não encontre caminho.

Se a cardinalidade final é `n`, imprime `mate[i] - n + 1` para cada jogador; caso contrário, `Impossible`.

Rastreio manual e análise de complexidade em [`acompanhamento/marco-3.md`](acompanhamento/marco-3.md).

---

## Implementação de referência

Tradução de [`HopcroftKarp.java`](../algs4-java/algs4/HopcroftKarp.java) do algs4. A `algs4-py` **não possui nenhum módulo de emparelhamento**, o que tornou a tradução necessária.

Foram preservados da referência o grafo com `2n` vértices, o laço de fases, `isResidualGraphEdge`, `isLevelGraphEdge` e a DFS com pilha explícita. As alterações restringem-se a equivalências de linguagem, à substituição do `BipartiteX` pela classe `Bipartition`, por a bipartição ser construída e não detectada, e à remoção do `inMinVertexCover`, não exigido pelo problema. Nenhuma lógica foi acrescentada.

Como as estruturas herdadas já estão em inglês, todo o código foi padronizado nesse idioma; a documentação permanece em português.

Alterações e justificativas detalhadas em [`acompanhamento/marco-4.md`](acompanhamento/marco-4.md).

---

## Casos especiais

| Caso | Entrada | Saída | O que verifica |
| :--- | :--- | :--- | :--- |
| Positivo mínimo | `2 1` / `1 2` | `2 1` | emparelhamento perfeito trivial |
| Jogador isolado | `3 1` / `1 2` | `Impossible` | atirador sem aresta nunca é emparelhado |
| Conexo sem solução | `3 2` / `1 2` / `2 3` | `Impossible` | **conexidade não implica solução** |
| Ciclo | `3 3` / `2 3` / `1 3` / `1 2` | `3 1 2` | atribuição cíclica, sem reciprocidade |
| Desconexo com solução | `6 6` (duas componentes) | `4 3 1 2 6 5` | **desconexão não implica `Impossible`** |

Toda saída é verificada como permutação de `1..n`, sem autodisparo e com todo disparo correspondendo a um par da entrada. Casos registrados em [`dados/casos-de-teste.txt`](dados/casos-de-teste.txt).

---

## Agradecimentos

Agradecemos ao **Prof. Me. Ricardo Carubbi** pelo acompanhamento dedicado a este problema, que envolveu orientação individual em momento extraclasse e a disponibilização de material complementar específico:

- [`notas_emparelhamento_maximo.md`](../mat-didatico/aulas/extras/notas_emparelhamento_maximo.md), publicado no repositório da disciplina;
- `paintball-rastreios.md`, com rastreios do `HopcroftKarp` e do `BipartiteMatching` sobre uma instância do problema;
- [Hopcroft-Karp em *Algorithms and Data Structures*, TU München](https://algorithms.discrete.ma.tum.de/graph-algorithms/matchings-hopcroft-karp/index_en.html), visualização interativa do algoritmo;
- [`A7_Problemas_Classicos.pdf`](../mat-didatico/aulas/A7_Problemas_Classicos.pdf), aula sobre emparelhamento apresentada antecipadamente para viabilizar este trabalho.

A orientação foi determinante para a compreensão do papel da BFS e da DFS no algoritmo e da relação entre emparelhamento e redes de fluxo.

---

## Declaração de uso de IA

O assistente Claude (Anthropic) foi utilizado como apoio de estudo e revisão ao longo do T2.
