## Marco 2 — Representação e validação
 
### 2.1 Justificativa da representação computacional
 
A representação adotada é a **lista de adjacência**, seguindo a implementação de
referência `EdgeWeightedGraph` da disciplina, em que cada vértice guarda um
conjunto das arestas incidentes a ele e cada aresta é registrada nas duas
pontas.
 
Justificativa:
 
- a estrutura é a da implementação de referência, o que mantém a adaptação
  próxima ao material da disciplina;
- o objeto aresta carrega os dois extremos e o peso juntos, que é exatamente o
  que o algoritmo de árvore geradora mínima consome;
- o algoritmo precisa percorrer as arestas incidentes a um vértice recém
  incorporado à árvore, e é essa a operação que a lista de adjacência atende
  diretamente.
**Ressalva registrada:** como o grafo é completo, a lista de adjacência não
obtém a economia que teria em um grafo esparso. Não existe ausência de aresta
para deixar de armazenar, então a lista ocupa `Θ(E)` com `E = m(m-1)/2`. A
estrutura foi mantida por fidelidade à referência, e o custo disso está
registrado na tabela abaixo.
 
Custo da representação:
 
| Operação | Complexidade | Valor com `m = 750` |
| --- | --- | --- |
| Espaço da lista de adjacência | `Θ(E) = Θ(m^2)` | 280.875 arestas |
| Construção do grafo | `Θ(m^2)` | 280.875 cálculos de distância |
| Percorrer as arestas de um vértice | `Θ(m)` | até 749 arestas |
| Cálculo de uma distância | `Θ(1)` | — |
 
### 2.2 Representação da instância pequena
 
Usando a instância do marco 1, com os vértices numerados `A = 0`, `B = 1`,
`C = 2`.
 
**Matriz de distâncias** (leitura humana, não é a estrutura usada):
 
|  | A | B | C |
| --- | --- | --- | --- |
| **A** | 0 | 1.000 | 1.000 |
| **B** | 1.000 | 0 | 1.414 |
| **C** | 1.000 | 1.414 | 0 |
 
A matriz é simétrica, porque o grafo é não dirigido, e tem diagonal nula.
 
**Lista de adjacência** (estrutura efetivamente utilizada):
 
```
3 vertices, 3 arestas
0: 0-1 1.00000  0-2 1.00000
1: 0-1 1.00000  1-2 1.41421
2: 0-2 1.00000  1-2 1.41421
```
 
Cada uma das 3 arestas aparece duas vezes, uma em cada extremo.
 
**Decisão sobre cada aresta:**
 
| Ponte | Comprimento | Decisão | Motivo |
| --- | --- | --- | --- |
| A–B | 1.000 | constrói | liga duas partes ainda separadas |
| A–C | 1.000 | constrói | liga duas partes ainda separadas |
| B–C | 1.414 | descarta | B e C já estão ligados através de A |
 
Total: `1.000 + 1.000 = 2.000`
 
### 2.3 Validação da entrada e da saída esperada
 
**Verificações de sanidade**
 
- o número de pontes construídas é sempre `m - 1`; na instância pequena, 2
  pontes para 3 ilhas;
- nenhuma ponte construída fecha ciclo;
- se `m = 1`, nenhuma ponte é construída e a saída é `0.000`, caso-limite da
  restrição `1 <= m`;
- critério de aceitação: `|resultado obtido - resultado esperado| <= 10^-3`.
**Casos de validação**
 
| Instância | Saída esperada |
| --- | --- |
| instância pequena (3 ilhas) | `2.000` |
| exemplo do enunciado, caso 2 (10 ilhas) | `168.010157...` |
 
**Caso de conferência do critério**
 
Uma instância construída para verificar que o critério não é simplesmente
"as pontes mais baratas". Três ilhas próximas e uma distante:
 
```
1
4
0.0 0.0
1.0 0.0
0.5 0.8
50.0 0.0
```
 
Com `A = (0,0)`, `B = (1,0)`, `C = (0.5,0.8)`, `D = (50,0)`:
 
| Ponte | Comprimento |
| --- | --- |
| A–C | 0.943 |
| B–C | 0.943 |
| A–B | 1.000 |
| B–D | 49.000 |
| C–D | 49.506 |
| A–D | 50.000 |
 
São necessárias 3 pontes. As três mais baratas seriam A–C, B–C e A–B, somando
`2.887`, mas elas formam um ciclo entre A, B e C e deixam D isolado. A resposta
correta é A–C, B–C e B–D, somando **50.887**.
 
A ponte A–B é recusada por ligar duas ilhas que já estavam conectadas através de
C. Este caso registra que o critério é "a aresta mais barata **que conecta algo
ainda não conectado**".
 
**Observação sobre unicidade:** quando há empate de comprimento, a árvore
escolhida pode variar, mas o **custo total é sempre o mesmo**. É isso que torna
a saída do problema bem definida.
 
### 2.4 Identificação preliminar da família
 
O problema pertence à família **árvore geradora mínima**.
 
Justificativa, termo a termo:
 
- **geradora**, porque a solução precisa alcançar todas as ilhas;
- **árvore**, porque qualquer ponte além das necessárias fecharia ciclo e seria
  custo sem ganho de conectividade;
- **mínima**, porque o critério de otimização é o comprimento total.
**Famílias descartadas**
 
| Família | Por que não se aplica |
| --- | --- |
| Caminho mínimo (Dijkstra, Bellman-Ford) | não existe vértice de origem nem de destino; o objetivo é conectar todas as ilhas, não ir de uma a outra |
| Fluxo máximo (Ford-Fulkerson, Edmonds-Karp) | exige capacidades nas arestas e uma fonte e um sumidouro, e aqui as arestas possuem apenas comprimento |
 
A escolha do algoritmo específico dentro da família e a sua justificativa ficam
registradas no Marco 3.
