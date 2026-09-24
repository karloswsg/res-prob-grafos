
# Marco 2 - Componentes Conexas: Paintball

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :------------------------- |
| 1.0     | 24/09/2026 | Criação do documento     |

---

## 1. Instância Particular (V=6, E=6)

O Marco 2 trabalha sobre o grafo **de entrada** do problema (relação de visão, não orientada), sem a duplicação em atiradores/alvos usada no Marco 1 — o objetivo aqui é identificar componentes conexas, não construir o emparelhamento.

Instância escolhida, respeitando o máximo V=6, E=6, grafo simples e não dirigido:

```text
Entrada:
6 6
1 2
1 3
1 4
2 3
2 4
5 6
```

Essa instância produz duas componentes conexas distintas: um "diamante" (K4 sem a aresta 3-4) entre os vértices {1,2,3,4} e um par isolado {5,6}, o que permite exercitar tanto o cálculo de excentricidades com valores desiguais quanto a detecção de mais de uma componente pelo algoritmo.

---

## 2. Desenho do Grafo e Listas de Adjacência

### Desenho

```text
    1 ─────── 4
    │ ╲     ╱ │
    │   ╲ ╱   │
    │   ╱ ╲   │
    │ ╱     ╲ │
    2 ─────── 3

    5 ─────── 6
```

(Representação textual do "diamante" 1-2-3-4, com a diagonal 1-2, e do par isolado 5-6, separado do restante.)

### Listas de adjacência

```text
1: 2, 3, 4
2: 1, 3, 4
3: 1, 2
4: 1, 2
5: 6
6: 5
```

### Componentes identificadas

```text
C1 = {1, 2, 3, 4}
C2 = {5, 6}
```

---

## 3. Excentricidades, Raio, Diâmetro, Vértices Centrais e Centro

Excentricidade, raio, diâmetro e centro são calculados **por componente conexa** — não existe distância entre vértices de componentes diferentes, então cada cálculo fica restrito aos vértices do mesmo componente.

### Excentricidades

```text
exc(1) = max{d(1,2), d(1,3), d(1,4)} = max{1, 1, 1} = 1
exc(2) = max{d(2,1), d(2,3), d(2,4)} = max{1, 1, 1} = 1
exc(3) = max{d(3,1), d(3,2), d(3,4)} = max{1, 1, 2} = 2
exc(4) = max{d(4,1), d(4,2), d(4,3)} = max{1, 1, 2} = 2
exc(5) = max{d(5,6)} = max{1} = 1
exc(6) = max{d(6,5)} = max{1} = 1
```

`d(3,4) = 2` e `d(4,3) = 2` porque não existe aresta 3-4 na instância; o menor caminho entre eles passa por 1 ou por 2.

### Raio e diâmetro

```text
raio(C1)    = min{exc(1), exc(2), exc(3), exc(4)} = min{1, 1, 2, 2} = 1
diâmetro(C1) = max{exc(1), exc(2), exc(3), exc(4)} = max{1, 1, 2, 2} = 2

raio(C2)    = min{exc(5), exc(6)} = min{1, 1} = 1
diâmetro(C2) = max{exc(5), exc(6)} = max{1, 1} = 1
```

### Vértices centrais e centro

Um vértice é central quando sua excentricidade é igual ao raio do seu componente; o centro é o conjunto desses vértices.

```text
vértice(s) centrais (C1) = 1, 2
centro(C1) = {1, 2}

vértice(s) centrais (C2) = 5, 6
centro(C2) = {5, 6}
```

---

## 4. Rastreamento Manual do Algoritmo de Componentes Conexas

### Estruturas de dados

- `adj[]`: lista de adjacência do grafo (já apresentada na Seção 2);
- `marked[]`: vetor booleano indicando se o vértice já foi visitado;
- `edgeTo[]`: vetor que guarda, para cada vértice visitado, a partir de qual vértice ele foi alcançado — registra a árvore de busca gerada pela DFS;
- `id[]` (implícito no algoritmo, não detalhado nas tabelas abaixo): identificador do componente ao qual cada vértice pertence, atribuído no momento em que uma nova DFS é iniciada a partir de uma fonte não visitada.

### Algoritmo (DFS recursiva)

```text
contador = 0
para cada vértice v de 1 a n:
    se marked[v] == falso:
        dfs(v, contador)
        contador = contador + 1

dfs(v, contador):
    marked[v] = verdadeiro
    id[v] = contador
    para cada w em adj[v]:
        se marked[w] == falso:
            edgeTo[w] = v
            dfs(w, contador)
```

O laço externo garante que todo vértice do grafo seja considerado: sempre que encontra um vértice ainda não marcado, esse vértice é a raiz de uma nova componente, e uma nova chamada de DFS é disparada com um identificador de componente novo. Vértices alcançados durante essa chamada recebem o mesmo `id`, o que é exatamente o critério de agrupamento em componentes.

### Rastreamento — fonte = 1

| V | edgeTo[] | marked[] |
| :-: | :------: | :------: |
| 1 |    -    |    V    |
| 2 |    1    |    V    |
| 3 |    2    |    V    |
| 4 |    2    |    V    |
| 5 |    -    |    F    |
| 6 |    -    |    F    |

Ordem de visita: 1 → 2 (via lista `1: 2,3,4`) → 3 (a partir de 2, pois 1 já está marcado) → volta a 2 → 4. Os vértices 5 e 6 permanecem não marcados porque não há aresta entre `{1,2,3,4}` e `{5,6}` — confirmando que essas duas componentes são de fato distintas.

### Rastreamento — fonte = 5

| V | edgeTo[] | marked[] |
| :-: | :------: | :------: |
| 5 |    -    |    V    |
| 6 |    5    |    V    |

Como todos os vértices já foram marcados ao final da fonte 1 exceto 5 e 6, o laço externo encontra o vértice 5 não visitado, inicia uma nova DFS (novo `id` de componente) e marca também o 6.

### Lógica de identificação das componentes

Cada chamada de DFS a partir do laço externo corresponde a exatamente uma componente conexa: todos os vértices marcados durante essa chamada recebem o mesmo `id`, e o número total de chamadas de DFS disparadas pelo laço externo é igual ao número de componentes do grafo. Nessa instância, houve duas chamadas (fonte 1 e fonte 5), confirmando `C1 = {1,2,3,4}` e `C2 = {5,6}`.

---

## 5. Complexidade de Tempo e Espaço; Custo das Consultas de Conectividade

### Tempo — pré-processamento (execução das DFS's)

- Cada vértice é marcado uma única vez e, uma vez marcado, nunca é revisitado — contribuição O(V).
- Para cada vértice visitado, percorre-se sua lista de adjacência inteira; somando sobre todos os vértices, cada aresta é examinada no máximo duas vezes (uma a partir de cada extremidade, pois o grafo é não dirigido) — contribuição O(E).
- Total: **O(V + E)**. Na instância (V=6, E=6): O(12).

### Espaço

- Lista de adjacência (estrutura do grafo): O(V + E);
- `marked[]`, `edgeTo[]` e `id[]`: O(V) cada;
- Pilha de recursão da DFS: O(V) no pior caso (profundidade máxima da árvore de busca);
- Total: **O(V + E)** (os termos O(V) são dominados pelo O(V+E) da lista de adjacência).

### Custo das consultas de conectividade

- **Antes do pré-processamento** (sem `id[]` calculado), responder "u e v estão no mesmo componente?" exigiria rodar uma busca a cada consulta — O(V+E) por consulta.
- **Depois do pré-processamento**, com `id[v]` atribuído a cada vértice durante a única passada de DFS's, a mesma consulta se resume a comparar `id[u] == id[v]` — **O(1)** por consulta.

O padrão geral é: pagar O(V+E) uma única vez para construir `id[]`, e a partir daí toda consulta de conectividade custa tempo constante — investimento inicial linear em troca de consultas praticamente gratuitas depois.
