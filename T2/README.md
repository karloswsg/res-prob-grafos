# Paintball (Kattis): Emparelhamento Perfeito com Hopcroft-Karp

**Grupo A · Problema I** · [open.kattis.com/problems/paintball](https://open.kattis.com/problems/paintball)
**Linguagem:** Python 3 · **Resultado:** `Accepted`, 0,06 s (limite de 3 s), 29/29 casos (submissão 20635412)

---

## O problema

`N` jogadores (2 ≤ N ≤ 1000) e `M` pares de visão (0 ≤ M ≤ 5000). Se `A` enxerga `B`, `B` também enxerga `A`. Cada jogador tem uma única bala e só pode atirar em quem enxerga. A pergunta: é possível que **todos sejam atingidos exatamente uma vez**? Se sim, imprimir o alvo de cada jogador (qualquer solução serve); se não, `Impossible`.

```text
Entrada:        Saída:
3 3             2
1 2             3
2 3             1
1 3
```

---

## Ideia central: a modelagem

O enunciado não fala de grafos. O passo decisivo foi reconhecer que cada jogador exerce **dois papéis independentes**: quem ele atinge e por quem é atingido. Desdobrando cada jogador em duas cópias, um grafo comum vira um grafo **bipartido**:

| Cópia         | Papel                            |
| :------------- | :------------------------------- |
| `i_atirador` | `i` como quem dispara          |
| `i_alvo`     | `i` como quem recebe o disparo |

Para cada par `a b` da entrada surgem duas arestas, `a_atirador → b_alvo` e `b_atirador → a_alvo`. O grafo modelado tem `2n` vértices e `2m` arestas, e a pergunta passa a ser: **existe emparelhamento perfeito** (todo atirador e todo alvo usados exatamente uma vez)?

Consequências que a análise do grafo mostrou:

- **Conexidade não decide a resposta.** Um grafo desconexo pode ter solução (cada componente se resolve sozinha) e um conexo pode não ter (`1–2`, `2–3`: os jogadores 1 e 3 só enxergam o 2).
- **Ciclos ímpares não atrapalham.** No triângulo, `1 → 2 → 3 → 1` é válido. Os disparos não precisam ser recíprocos, porque o emparelhamento ocorre entre cópias, não entre jogadores.
- A validade da solução depende de uma condição que o enunciado não declara explicitamente: a relação de visão é **simétrica**.

---

## Algoritmo

### De DFS simples a Hopcroft-Karp

A primeira versão pensada buscava **um caminho aumentante por atirador livre** (DFS), com custo `O(V·E)`. Como a linguagem é Python, de custo por operação alto, optou-se pela variante **por fases**, o Hopcroft-Karp, com custo `O(E√V)`.

**Caminho aumentante:** caminho que parte de um atirador livre, alterna arestas fora e dentro do emparelhamento e termina em um alvo livre. Inverter as arestas ao longo dele aumenta o emparelhamento em uma unidade. O emparelhamento é máximo quando não existe nenhum.

**Cada fase:**

1. **BFS** a partir de *todos* os atiradores livres ao mesmo tempo, calculando o nível (`dist`) de cada atirador.
2. **DFS** restrita a arestas que sobem exatamente um nível (`dist[u] == dist[v] + 1`), extraindo o maior conjunto possível de caminhos aumentantes mínimos e disjuntos.
3. Repete até que uma fase não encontre caminho algum.

**Resposta:** se a cardinalidade final é `n`, imprime `mate_shooter[i]` para cada jogador; caso contrário, `Impossible`.

### Exemplo rastreado (6 jogadores)

```text
6 6
1 2    1 3    1 4
2 3    2 4    5 6
```

| Fase | O que acontece                                                                                                                                                | Cardinalidade |
| :--: | :------------------------------------------------------------------------------------------------------------------------------------------------------------ | :-----------: |
|  1  | todos livres (`dist = 0`); caminhos de comprimento 1 emparelham `1→2`, `2→1`, `5→6`, `6→5`; os atiradores 3 e 4 só enxergam 1 e 2, já tomados |       4       |
|  2  | livres: 3 e 4.`3 → alvo 1 (de 2) → 2 passa a atirar em 3`; `4 → alvo 2 (de 1) → 1 passa a atirar em 4`. Dois caminhos de comprimento 3, disjuntos     |       6       |
|  3  | sem atiradores livres; encerra                                                                                                                                |       6       |

Saída: `4 3 1 2 6 5`. Na fase 2, o atirador 2 **já estava emparelhado** e mesmo assim trocou de alvo: é isso que distingue o caminho aumentante de uma simples busca por vaga livre.

---

## Implementação (`src/main.py`)

Adaptação do `HopcroftKarp.java` do algs4. A `algs4-py` **não possui nenhum módulo de emparelhamento** (foram verificados os 30 módulos), então a base é a versão Java traduzida para Python.

| Estrutura           | Papel                                                                                         |
| :------------------ | :-------------------------------------------------------------------------------------------- |
| `adj[v]`          | lista de adjacência da relação de visão (`n` listas)                                    |
| `mate_shooter[v]` | alvo em que`v` atira; é a própria saída                                                  |
| `mate_target[w]`  | quem atira em`w`; permite continuar o caminho alternado                                     |
| `dist[v]`         | nível do atirador`v` na fase; `INF` se inalcançável (também serve de marca de visita) |
| `cardinality`     | atiradores emparelhados                                                                       |

| Método                  | Responsabilidade                                                                                                                            |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `_has_augmenting_path` | BFS de fase                                                                                                                                 |
| `_dfs`                 | DFS no grafo de níveis; ao falhar, marca`dist[v] = INF` para não reexplorar o vértice na fase (sem isso o limite `O(E√V)` se perde) |
| `is_perfect`           | `cardinality == n`                                                                                                                        |
| `main`                 | leitura em bloco, construção de`adj`, saída em uma string                                                                              |

### O que mudou em relação à referência

Nenhuma lógica foi acrescentada: só traduções, simplificações e remoções.

| Alteração                                                                                                                | Motivo                                                                                |
| :------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `mate[]` de tamanho `2n` → dois vetores de tamanho `n`                                                              | papéis separados tornam o sentido da travessia implícito                            |
| `isResidualGraphEdge()` eliminado                                                                                        | consequência direta da separação acima                                             |
| `isLevelGraphEdge()` → `dist[u] == dist[v] + 1`                                                                       | comparação direta                                                                   |
| `BipartiteX` descartado                                                                                                  | a bipartição é**construída**, não detectada                                |
| `inMinVertexCover[]` descartado                                                                                          | cobertura mínima (teorema de König) não é exigida                                 |
| `isPerfect()` → `cardinality == n`                                                                                    | os dois lados têm tamanho`n`                                                       |
| `Integer.MAX_VALUE` → `float('inf')`; `Queue` → `deque`; `StdIn/StdOut` → `sys.stdin.buffer`/`sys.stdout` | idiomas de Python                                                                     |
| **Buscas partem dos atiradores livres** (a referência parte dos alvos)                                              | escolha simétrica: a resposta continua válida, mas muda qual solução é produzida |

**Recursão:** a DFS é recursiva como na referência. A profundidade é limitada pelo comprimento do caminho aumentante da fase, que é `O(√V)` (cerca de 32 níveis para `n = 1000`).

**Índices:** a entrada usa `1..n`, os vetores usam `0..n-1`; a conversão é feita na leitura e desfeita na saída.

### Referências do algs4 consideradas

| Referência                | Decisão                                                                                                                          |
| :------------------------- | :-------------------------------------------------------------------------------------------------------------------------------- |
| `HopcroftKarp.java`      | **adaptada** (núcleo)                                                                                                      |
| `graph.py`               | **reutilizada** (lista de adjacência, como lista de listas nativa)                                                         |
| `BipartiteMatching.java` | descartada (`O(V·E)`)                                                                                                          |
| `BipartiteX.java`        | descartada (bipartição já conhecida)                                                                                           |
| `AssignmentProblem.java` | descartada (o problema não tem pesos)                                                                                            |
| `cc.py`                  | descartada: a checagem antecipada de`Impossible` é desnecessária, pois o próprio algoritmo termina com cardinalidade `< n` |

---

## Complexidade

| Aspecto           | Custo                                                                 |
| :---------------- | :-------------------------------------------------------------------- |
| Tempo             | `O(E√V)`: `O(√V)` fases, cada uma com BFS + DFS em `O(V + E)` |
| Memória do grafo | `O(V + E)`: `V` listas e `2E` entradas                          |
| Memória auxiliar | `O(V)`: `mate_shooter`, `mate_target`, `dist`, fila e pilha   |

O número de fases é `O(√V)` porque o comprimento do menor caminho aumentante cresce a cada fase. Nenhuma estrutura auxiliar cresce com o número de arestas: o algoritmo as percorre, mas não as armazena. A adaptação é ainda mais econômica que a referência, que mantém um grafo de `2n` vértices.

### Componentes conexas (apoio de análise)

Sobre o grafo de entrada, a DFS com `marked[]`, `edgeTo[]` e `id[]` identifica as componentes em `O(V + E)`, e depois disso cada consulta "`u` e `v` estão na mesma componente?" custa `O(1)` (`id[u] == id[v]`). Na instância de 6 vértices, duas chamadas de DFS (fontes 1 e 5) revelam `C1 = {1,2,3,4}` e `C2 = {5,6}`. Excentricidades, raio e diâmetro são calculados por componente (C1: raio 1, diâmetro 2, centro `{1,2}`; C2: raio 1, diâmetro 1, centro `{5,6}`). Esse recurso acabou **não sendo necessário** na solução final.

---

## Testes

Casos registrados em `dados/casos-de-teste.txt`.

| Caso                    | Entrada                               | Saída          | O que verifica                            |
| :---------------------- | :------------------------------------ | :-------------- | :---------------------------------------- |
| Positivo                | `2 1` / `1 2`                     | `2` `1`     | emparelhamento perfeito mínimo           |
| Vértice isolado        | `3 1` / `1 2`                     | `Impossible`  | atirador sem arestas nunca é emparelhado |
| Conexo sem solução    | `3 2` / `1 2` / `2 3`           | `Impossible`  | conexidade não implica solução         |
| Ciclo                   | `3 3` / `2 3` / `1 3` / `1 2` | `3 1 2`       | atribuição cíclica, sem reciprocidade  |
| Desconexo com solução | instância de 6 jogadores acima       | `4 3 1 2 6 5` | desconexão não implica`Impossible`    |

**Verificações aplicadas a toda saída:** é uma permutação de `1..n` (cada jogador atingido exatamente uma vez); ninguém atira em si mesmo (não há laços); todo disparo corresponde a um par da entrada.

---

## Relação com fluxo máximo

Emparelhamento bipartido é um caso particular de fluxo máximo com capacidades unitárias. A rede equivalente acrescenta uma fonte `S` e um destino `D`:

```text
S → atirador i (cap. 1)  →  alvo j (cap. 1)  →  D (cap. 1)
```

Cada unidade de fluxo é uma decisão de disparo, e o fluxo máximo iguala a cardinalidade do emparelhamento máximo. As fases do Hopcroft-Karp correspondem à estratégia de fases em redes de capacidade unitária. **A modelagem por fluxo não foi implementada**: com capacidades unitárias e rede bipartida, o emparelhamento resolve diretamente.

**Coloração** e **isomorfismo** não se aplicam. O grafo construído é 2-colorível, mas isso é consequência da modelagem, não exigência do enunciado; e não há comparação entre estruturas.

---

## Conclusão

- A etapa determinante foi a **modelagem**, não o algoritmo: desdobrar cada jogador em atirador e alvo transforma o problema em existência de emparelhamento perfeito.
- Estabelecida a modelagem, a implementação consistiu sobretudo em **remover o que a referência oferece a mais** e traduzi-la para Python.
- A escolha pela versão por fases (`O(E√V)`) em vez da busca simples (`O(V·E)`) foi motivada pelo custo de Python; com os limites do problema, o tempo medido (0,06 s de 3 s) mostra folga ampla.

---
