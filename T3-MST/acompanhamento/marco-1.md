**Integrantes:** Maria Eduarda Coutinho Angelim (2324319), Karlos Eduardo (2320262)
 
---
 
## Marco 1 — Formulação
 
### 1.1 Resumo do problema
 
Um país é formado por várias ilhas espalhadas no oceano. Hoje os habitantes se
deslocam apenas de barco, e o governo quer construir pontes para ligar todas as
ilhas entre si.
 
O custo de uma ponte é proporcional ao seu comprimento. O governo quer gastar o
mínimo possível, então precisa decidir **quais pontes construir** para que toda
ilha fique alcançável a partir de qualquer outra, com o menor comprimento total
de ponte.
 
A entrada informa apenas a posição de cada ilha. A saída é o comprimento total
do conjunto de pontes escolhido.
 
Observação importante da leitura do enunciado: o problema **não pede um caminho
entre duas ilhas**. Ele pede quais ligações passam a existir.
 
### 1.2 Entrada, saída, objetivo e restrições
 
**Entrada**
 
- primeira linha: um inteiro `n`, o número de casos de teste;
- cada caso começa com uma linha contendo `m`, o número de ilhas;
- em seguida, `m` linhas com dois valores reais `x y`, a posição da ilha.
**Saída**
 
- para cada caso de teste, o comprimento total das pontes necessárias para
  conectar todas as ilhas.
**Objetivo**
 
- minimizar a soma dos comprimentos das pontes construídas, garantindo que
  todas as ilhas fiquem conectadas.
**Restrições**
 
| Parâmetro | Limite |
| --- | --- |
| Casos de teste | `1 <= n <= 10` |
| Ilhas por caso | `1 <= m <= 750` |
| Coordenadas | reais em `[-1000, 1000]`, até 3 casas decimais |
| Pontos | todos distintos |
| Tolerância da saída | erro relativo e absoluto de até `10^-3` |
| Tempo | 3 s |
| Memória | 1024 MB |
 
O enunciado imprime `2.000` em um caso e `168.01015709273446` em outro, o que
confirma que a comparação da saída é numérica e não textual.
 
### 1.3 Modelagem em grafo
 
| Elemento do grafo | Correspondência no problema |
| --- | --- |
| Vértice | uma ilha |
| Aresta | uma ponte possível entre duas ilhas |
| Direção | não dirigido, a ponte serve nos dois sentidos |
| Peso | distância euclidiana entre as duas ilhas |
| Capacidade | não se aplica, não é um problema de fluxo |
 
O peso de cada aresta é
 
```
d(i, j) = raiz( (xj - xi)^2 + (yj - yi)^2 )
```
 
**O grafo é completo.** Qualquer ilha pode ser ligada a qualquer outra, logo
existem `m(m-1)/2` arestas candidatas. Com `m = 750`, são **280.875** pontes
possíveis.
 
As arestas **não aparecem na entrada**. Elas são deduzidas das coordenadas.
 
### 1.4 Instância pequena
 
```
1
3
0.0 0.0
0.0 1.0
1.0 0.0
```
 
Vértices: `A = (0,0)`, `B = (0,1)`, `C = (1,0)`
 
Arestas candidatas:
 
| Ponte | Comprimento |
| --- | --- |
| A–B | 1.000 |
| A–C | 1.000 |
| B–C | 1.414 |
 
Saída esperada: **2.000**
 
---
