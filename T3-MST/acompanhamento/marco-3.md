# Marco 3: Escolha do algoritmo

**Disciplina:** Resolução de Problemas com Grafos
**Orientador:** Prof. Me. Ricardo Carubbi
**Trabalho Prático 3, classe Árvore Geradora Mínima**
**Problema B:** Kattis Island Hopping (<https://open.kattis.com/problems/islandhopping>)

**Integrantes:** Maria Eduarda Coutinho Angelim (2324319), Karlos Eduardo (2320262)

---

## 3.1 Algoritmo escolhido e justificativa

O algoritmo escolhido é o **Prim na versão lazy**, adaptado da implementação de
referência `LazyPrimMST` do algs4.

### Representação consumida pelo algoritmo

O algoritmo opera sobre a **matriz de consulta** definida no Marco 2:
`M[i][j]` guarda a distância euclidiana entre as ilhas `i` e `j`, com consulta
em `O(1)`. Como o grafo é completo, **a linha `v` da matriz é a vizinhança de
`v`**: percorrer a linha equivale a percorrer todas as pontes que saem da ilha.

### Ideia

O algoritmo mantém dois grupos de ilhas: as que já fazem parte da árvore e as
que ainda estão de fora. A cada passo ele escolhe a ponte mais barata que liga
os dois grupos, e a ilha alcançada passa para o grupo da árvore. Começa com uma
única ilha na árvore e termina quando todas foram alcançadas.

### Estruturas

| Estrutura | Papel |
| --- | --- |
| `marked[]` | vetor booleano; `marked[v]` é verdadeiro quando a ilha `v` já está na árvore. É o que impede a formação de ciclo |
| `pq` | fila de prioridade mínima com as pontes candidatas; a operação relevante é remover a de menor peso |
| `mst` e `weight` | pontes aceitas e a soma dos pesos, que é a saída do problema |

### Funcionamento

```
visit(v):
    marked[v] = verdadeiro
    para cada ilha w na linha v da matriz:
        se w não está marcada:
            insere a ponte (v, w, M[v][w]) na fila

prim():
    visit(0)
    enquanto a fila não estiver vazia:
        e = remove o mínimo da fila
        v, w = extremos de e
        se marked[v] e marked[w]:
            descarta e                 (ponte obsoleta)
        senão:
            aceita e na mst
            weight = weight + peso de e
            visit(extremo ainda não marcado)
```

O nome **lazy** vem do tratamento das pontes obsoletas. Quando uma ilha entra
na árvore, as pontes antigas que apontavam para ela deixam de ser úteis, mas
não são retiradas da fila naquele momento. Elas só são percebidas e descartadas
quando chegam ao topo.

### Por que Prim e não Kruskal

| Critério | Kruskal | Prim lazy |
| --- | --- | --- |
| Ponto de partida | lista de todas as arestas, ordenada | uma ilha e a linha dela na matriz |
| Detecção de ciclo | estrutura union-find | consulta direta a `marked[]` |
| Relação com a matriz de consulta | precisa converter a matriz em lista de arestas antes de começar | consome a matriz diretamente, uma linha por visita |
| Tempo | `O(E log E)` | `O(E log E)` |

Os dois têm a mesma ordem de complexidade de tempo, então a escolha **não** se
apoia em desempenho assintótico. Ela se apoia em adequação à representação: as
arestas não vêm na entrada, são deduzidas das coordenadas, e o Prim as consulta
na matriz à medida que precisa, sem a etapa de materializar e ordenar as
280.875 arestas do pior caso e sem uma segunda estrutura para detectar ciclos.

### Por que lazy e não eager

| Critério | Prim eager | Prim lazy |
| --- | --- | --- |
| O que a fila guarda | no máximo uma ponte por ilha de fora (a melhor conhecida) | todas as pontes candidatas, inclusive as obsoletas |
| Tamanho máximo da fila | `V` | `E` |
| Fila necessária | fila indexada com operação de diminuir chave | fila de prioridade mínima simples |
| Tempo | `O(E log V)` | `O(E log E)` |
| Espaço extra | `O(V)` | `O(E)` |

No grafo completo `E = m(m-1)/2`, então `log E` é aproximadamente `2 log m`, e
as duas versões ficam na mesma ordem de tempo, `O(m^2 log m)`. A diferença real
é o espaço. Como o pior caso tem 280.875 arestas e o limite de memória é de
1024 MB, o custo de espaço da versão lazy é aceitável, e ela foi preferida por
usar uma fila mais simples, mais fácil de adaptar e de rastrear manualmente.

---

## 3.2 Condições de aplicabilidade

| Condição do algoritmo | Situação no problema |
| --- | --- |
| Grafo não dirigido | atende: a ponte serve nos dois sentidos |
| Grafo ponderado | atende: o peso é a distância euclidiana |
| Grafo conexo | atende: o grafo é completo, logo sempre conexo |
| Pesos | podem ser quaisquer reais (a MST admite inclusive pesos negativos); aqui são distâncias, todas positivas, pois os pontos são distintos |

Observações:

- se o grafo não fosse conexo, não existiria árvore geradora, e o resultado
  seria uma floresta geradora mínima; a implementação de referência trata isso
  reiniciando o Prim em cada vértice ainda não marcado, mas esse caso não
  ocorre neste problema;
- com pesos todos distintos a MST é única; com empates pode existir mais de uma
  árvore, todas com o **mesmo custo total**, que é o que o problema pede;
- caso-limite `m = 1`: a única ilha é marcada, nenhuma ponte é inserida, a
  árvore fica vazia e a saída é `0`.

---

## 3.3 Invariante, propriedade e operação central

### Propriedade do corte

Um corte é uma divisão dos vértices em dois grupos não vazios. A propriedade do
corte afirma que **a aresta de menor peso que cruza um corte qualquer pertence
a uma árvore geradora mínima**.

Justificativa resumida: os dois grupos precisam ser ligados por alguma aresta.
Se uma árvore geradora usasse uma aresta de cruzamento mais cara que a mínima,
adicionar a mínima fecharia um ciclo que cruza o corte pelo menos duas vezes, e
remover a mais cara desse ciclo produziria uma árvore de custo menor ou igual.

### Invariante

A cada iteração do Prim:

1. as pontes aceitas formam uma árvore que conecta exatamente as ilhas
   marcadas;
2. essa árvore é subconjunto de alguma árvore geradora mínima;
3. toda ponte que cruza o corte entre ilhas marcadas e não marcadas está na
   fila (junto com, possivelmente, pontes obsoletas).

O invariante se mantém porque a ponte removida do topo, quando não é obsoleta,
é a mais barata que cruza o corte atual, e pela propriedade do corte ela
pertence a uma MST. Como exatamente um dos extremos está fora da árvore,
aceitá-la nunca fecha ciclo.

### Operação central

Remover o mínimo da fila e testar os dois extremos em `marked[]`:

- os dois marcados: a ponte é **obsoleta** e é **descartada**;
- apenas um marcado: a ponte é **aceita**, o peso é acumulado e o extremo de
  fora é **visitado**, o que o marca e insere as pontes dele na fila.

---

## 3.4 Execução manual

### Instância

```
1
5
0.0 4.0
6.0 6.0
1.0 0.0
0.0 6.0
5.0 8.0
```

Ilhas: `A = (0,4)`, `B = (6,6)`, `C = (1,0)`, `D = (0,6)`, `E = (5,8)`

### Matriz de consulta

|  | A | B | C | D | E |
| --- | --- | --- | --- | --- | --- |
| **A** | 0 | 6.325 | 4.123 | 2.000 | 6.403 |
| **B** | 6.325 | 0 | 7.810 | 6.000 | 2.236 |
| **C** | 4.123 | 7.810 | 0 | 6.083 | 8.944 |
| **D** | 2.000 | 6.000 | 6.083 | 0 | 5.385 |
| **E** | 6.403 | 2.236 | 8.944 | 5.385 | 0 |

### Rastreamento

A fila é mostrada em ordem crescente para facilitar a leitura. O heap garante
apenas que o mínimo está no topo.

| Passo | Operação | Fila após a operação | MST | Peso |
| --- | --- | --- | --- | --- |
| 0 | `visit(A)`: marca A; insere AD, AC, AB, AE | AD 2.000, AC 4.123, AB 6.325, AE 6.403 | vazia | 0 |
| 1 | remove AD; A marcado e D não: aceita. `visit(D)`: marca D; insere DE, DB, DC; DA não é inserida, pois A já está marcado | AC 4.123, DE 5.385, DB 6.000, DC 6.083, AB 6.325, AE 6.403 | AD | 2.000 |
| 2 | remove AC; A marcado e C não: aceita. `visit(C)`: marca C; insere CB, CE | DE 5.385, DB 6.000, DC 6.083, AB 6.325, AE 6.403, CB 7.810, CE 8.944 | AD, AC | 6.123 |
| 3 | remove DE; D marcado e E não: aceita. `visit(E)`: marca E; insere EB | EB 2.236, DB 6.000, DC 6.083, AB 6.325, AE 6.403, CB 7.810, CE 8.944 | AD, AC, DE | 11.508 |
| 4 | remove EB; E marcado e B não: aceita. `visit(B)`: marca B; não insere nada | DB 6.000, DC 6.083, AB 6.325, AE 6.403, CB 7.810, CE 8.944 | AD, AC, DE, EB | 13.744 |
| 5 a 10 | remove DB, DC, AB, AE, CB e CE, nessa ordem; em todas os dois extremos já estão marcados: descarta | vazia | AD, AC, DE, EB | 13.744 |

Ordem em que as ilhas foram marcadas: A, D, C, E, B.

Resultado: 4 pontes, que é `m - 1`, e peso total **13.744**.

### Observações sobre a execução

- **Comportamento lazy:** a ponte DC entra na fila no passo 1, quando C ainda
  estava de fora. No passo 2 a ilha C entra na árvore por AC, e DC se torna
  obsoleta, mas permanece na fila até ser removida e descartada no final.
- **O algoritmo só enxerga o corte:** EB (2.236) é a segunda menor aresta do
  grafo inteiro, mas é a última a ser aceita, porque só entra na fila quando E
  é visitada. O Prim não ordena todas as arestas; ele compara apenas as que
  saem da árvore já construída.
- **Filtro do `visit`:** das 20 consultas possíveis à matriz fora da diagonal,
  apenas 10 geram inserção. Cada ponte é inserida uma única vez, na visita do
  primeiro extremo que entra na árvore.

---

## 3.5 Complexidade

Notação: `V` vértices, `E` arestas, `m` ilhas; no grafo completo `V = m` e
`E = m(m-1)/2`.

### Tempo

- cada ponte é inserida na fila **exatamente uma vez**, na visita do primeiro
  extremo marcado;
- cada ponte é removida da fila **no máximo uma vez**;
- cada inserção ou remoção em um heap binário custa `O(log n)`, com `n` o
  tamanho da fila, que é no máximo `E`;
- as visitas percorrem uma linha da matriz por ilha: `m` linhas de `m`
  posições, `O(m^2)` no total, o que não domina.

Total: `O(E log E)`.

### Espaço

- a fila pode conter até `E` pontes, pois as obsoletas não são retiradas no
  momento em que deixam de servir: `O(E)`;
- `marked[]` ocupa `O(V)`;
- a matriz de consulta ocupa `O(m^2)`.

### No problema

| Medida | Geral | Em função de `m` | Pior caso, `m = 750` |
| --- | --- | --- | --- |
| Arestas | `E` | `m(m-1)/2` | 280.875 |
| Tempo | `O(E log E)` | `O(m^2 log m)` | heap com cerca de 18 níveis de altura (`log2 E`) |
| Espaço da fila | `O(E)` | `O(m^2)` | até 280.875 pontes |
| Matriz de consulta | | `O(m^2)` | 562.500 valores |
| Construção da matriz | | `O(m^2)` | 280.875 distâncias calculadas |

A entrada tem até 10 casos de teste, e cada caso é resolvido de forma
independente, então o custo total é a soma dos custos por caso.

---

## 3.6 Pontos de atenção para o Marco 4

Registrados aqui para orientar a adaptação da implementação de referência:

- a referência recebe um `EdgeWeightedGraph`; a adaptação fará o `visit`
  percorrer a linha da matriz de consulta em vez da lista de adjacência;
- a referência esvazia a fila até o fim, removendo e descartando as pontes
  obsoletas restantes. O próprio código de referência em Java registra, em
  comentário, que é melhor parar quando a MST atinge `V - 1` arestas. Essa
  parada antecipada será avaliada na adaptação, com medição;
- a saída deve ser impressa com precisão suficiente para a tolerância de
  `10^-3` do enunciado.
