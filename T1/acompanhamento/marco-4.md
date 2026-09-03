# Marco 4 - Aplicação Básica de BFS e Conclusão: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 03/09/2026 | Criação do documento: execução manual da BFS na instância 3×3, níveis, distâncias, predecessores, comparação com a DFS, escolha justificada, adaptação da referência, testes, complexidade, submissão aceita e ensaio |

---

## 1. Instância e Ponto de Partida

Instância: **tabuleiro 3×3**, a mesma dos Marcos 1 a 3, com as 9 casas numeradas de `0` a `8`, linha a linha. Origem da busca: vértice **0** — idêntica à do Marco 3, o que torna as duas execuções diretamente comparáveis.

| Vértice | Vizinhos |     | Vértice | Vizinhos |
| :-----: | :------- | :-: | :-----: | :------- |
| 0       | 5, 7     |     | 5       | 0, 6     |
| 1       | 6, 8     |     | 6       | 1, 5     |
| 2       | 3, 7     |     | 7       | 0, 2     |
| 3       | 2, 8     |     | 8       | 1, 3     |
| 4       | (vazia)  |     |         |          |

---

## 2. Execução Manual

A BFS mantém uma **fila FIFO**. A origem é marcada e enfileirada com distância 0. A cada iteração um vértice é desenfileirado e seus vizinhos ainda não marcados são marcados, recebem predecessor e distância, e entram no fim da fila.

| Passo | Desenfileira | Vizinhos descobertos | `dist` atribuída | Fila após o passo |
| :---: | :----------: | :------------------- | :--------------: | :---------------- |
| 1     | 0            | 5, 7                 | 1                | `5 7`             |
| 2     | 5            | 6                    | 2                | `7 6`             |
| 3     | 7            | 2                    | 2                | `6 2`             |
| 4     | 6            | 1                    | 3                | `2 1`             |
| 5     | 2            | 3                    | 3                | `1 3`             |
| 6     | 1            | 8                    | 4                | `3 8`             |
| 7     | 3            | —                    | —                | `8`               |
| 8     | 8            | —                    | —                | vazia             |

Nos passos 7 e 8 nenhum vértice é descoberto: todos os vizinhos de `3` e de `8` já estavam marcados. A fila esvazia e a busca encerra. O vértice `4` nunca é enfileirado.

**Momento da marcação.** O vértice é marcado no instante da **descoberta**, e não quando sai da fila. Sem isso, um mesmo vértice poderia ser enfileirado mais de uma vez — uma por vizinho que o alcançasse — e a busca deixaria de ser linear.

---

## 3. Níveis, Distâncias e Predecessores

| Vértice | `marked[v]` | `dist[v]` | Nível | Predecessor `edgeTo[v]` |
| :-----: | :---------- | :-------: | :---: | :---------------------: |
| 0       | `true`      | 0         | 0     | — (origem)              |
| 5       | `true`      | 1         | 1     | 0                       |
| 7       | `true`      | 1         | 1     | 0                       |
| 6       | `true`      | 2         | 2     | 5                       |
| 2       | `true`      | 2         | 2     | 7                       |
| 1       | `true`      | 3         | 3     | 6                       |
| 3       | `true`      | 3         | 3     | 2                       |
| 8       | `true`      | 4         | 4     | 1                       |
| **4**   | **`false`** | **∞**     | —     | —                       |

Agrupando por nível:

```
nível 0:  { 0 }
nível 1:  { 5, 7 }
nível 2:  { 6, 2 }
nível 3:  { 1, 3 }
nível 4:  { 8 }
```

A árvore de caminhos mínimos **ramifica na origem**: o vértice `0` possui dois filhos, `5` e `7`. A busca percorre o ciclo simultaneamente nos dois sentidos, e os ramos se encontram em `8`, o vértice diametralmente oposto à origem — o que explica ser ele o mais distante, a 4 arestas.

**Arestas da árvore:** `0–5`, `0–7`, `5–6`, `7–2`, `6–1`, `2–3`, `1–8` — sete arestas para oito vértices alcançados (`V − 1`).

**Aresta fora da árvore:** `3–8`. Ao desenfileirar `3`, o vértice `8` já havia sido marcado, descoberto a partir de `1` no passo 6, e a aresta foi descartada. Note-se que a aresta descartada pela DFS, no Marco 3, foi `0–7` — outra aresta do mesmo grafo, confirmando que a árvore de busca depende do algoritmo, e não apenas do grafo.

O valor `∞` de `dist[4]` representa a ausência de caminho e corresponde a `marked[4] = false`. Na implementação, é o valor inicial do vetor de distâncias.

---

## 4. Comparação entre DFS e BFS

Ambas as execuções partem do vértice `0` no mesmo grafo, com a mesma lista de adjacência.

### Mecanismo

| Aspecto | DFS (Marco 3) | BFS (Marco 4) |
| :--- | :--- | :--- |
| Estrutura de controle | pilha (implícita na recursão) | fila FIFO (explícita) |
| Forma do algoritmo | recursão | laço `while` |
| Comportamento | aprofunda um ramo até esgotá-lo | expande por níveis de distância |
| Vetores auxiliares | `marked`, `edgeTo` | `marked`, `edgeTo`, **`dist`** |
| Ordem de visita | por profundidade | por **distância crescente** à origem |
| Complexidade | `O(V + E)` | `O(V + E)` |

As duas buscas têm **o mesmo custo assintótico**. A escolha entre elas não envolve compromisso de desempenho.

### Resultado

| Aspecto | DFS | BFS |
| :--- | :--- | :--- |
| Forma da árvore | caminho sem ramificação | árvore com dois ramos a partir da origem |
| Árvore obtida | `0-5-6-1-8-3-2-7` | ramifica em `5` e `7` |
| Aresta descartada | `0–7` | `3–8` |
| Vértices alcançados | 8 (todos menos `4`) | 8 (todos menos `4`) |

A **alcançabilidade é idêntica**: ambas marcam os mesmos oito vértices e deixam `4` de fora. Para responder se existe caminho, as duas servem igualmente.

A diferença está no **comprimento** dos caminhos produzidos:

| Consulta | DFS | BFS | Distância real | DFS confere? |
| :------- | :-: | :-: | :------------: | :----------: |
| `0 → 5`  | 1   | 1   | 1              | sim          |
| `0 → 7`  | 7   | 1   | 1              | **não**      |
| `0 → 6`  | 2   | 2   | 2              | sim          |
| `0 → 2`  | 6   | 2   | 2              | **não**      |
| `0 → 1`  | 3   | 3   | 3              | sim          |
| `0 → 3`  | 5   | 3   | 3              | **não**      |
| `0 → 8`  | 4   | 4   | 4              | sim          |
| `0 → 4`  | —   | —   | sem caminho    | sim          |

A BFS acerta as oito consultas. A DFS erra três, sendo `0 → 7` o caso mais expressivo: os dois vértices são adjacentes — um único movimento — e a DFS percorre sete arestas até alcançá-lo.

O padrão dos erros é sistemático: a DFS acerta exatamente os vértices do ramo em que mergulhou (`5`, `6`, `1`, `8`) e erra os do ramo oposto (`7`, `2`, `3`), alcançados apenas após percorrer quase todo o ciclo.

---

## 5. Escolha Justificada

**Algoritmo escolhido: Busca em Largura (BFS).**

**1. A BFS garante o caminho mínimo; a DFS não.** A fila FIFO assegura que os vértices sejam processados na ordem em que entram, de modo que todos os vértices a distância `k` são descobertos antes de qualquer vértice a distância `k+1`. Quando um vértice é alcançado pela primeira vez, todos os vértices mais próximos da origem já foram processados sem alcançá-lo — logo, não existe caminho mais curto. A primeira chegada é, portanto, a chegada mínima. A DFS não oferece garantia análoga: o caminho que produz é o do mergulho corrente, cujo comprimento não guarda relação com a distância.

**2. A garantia da BFS independe da ordem de armazenamento.** Conforme registrado no Marco 3, a árvore da DFS se altera com a ordem dos vizinhos na lista de adjacência: invertendo `adj[0]` de `5, 7` para `7, 5`, o caminho até `7` passaria de sete arestas para uma. Na BFS os níveis permanecem os mesmos sob qualquer ordenação — apenas o predecessor registrado pode variar em caso de empate entre dois vértices do mesmo nível, sem afetar a distância. Um resultado sensível à ordem de armazenamento não pode ser qualificado como mínimo.

**3. Não há custo associado à escolha.** Ambos os algoritmos são `O(V + E)`. A BFS ainda produz diretamente o vetor `dist[]`, que é exatamente a saída exigida pelo problema.

**Condição de validade.** A BFS garante o caminho mínimo porque o grafo é **não ponderado** — toda aresta corresponde a um movimento de custo unitário. Caso os movimentos tivessem custos distintos, a contagem de arestas deixaria de responder ao menor custo, e seria necessário um algoritmo de caminho de custo mínimo, como Dijkstra, com fila de prioridade no lugar da fila comum.

**Aproveitamento da DFS.** A DFS permanece útil para alcançabilidade e identificação de componentes conexas, para detecção de ciclo por aresta de retorno, e para reconstruir *um* caminho quando a minimalidade não é exigida — conforme registrado no Marco 3.

---

## 6. Adaptação e Integração

Base: `algs4-py/algs4/graph.py` e `algs4-py/algs4/breadth_first_paths.py`, do repositório da disciplina.

### Adaptações realizadas

**1. Construção implícita do grafo.** A referência lê ordem, tamanho e lista de arestas de um arquivo. Como o grafo do problema é fixo e definido pela regra de movimento, essa leitura foi substituída pela função `constroi_tabuleiro()`, que percorre as 64 casas, aplica os 8 deslocamentos do cavalo e descarta os que caem fora do tabuleiro. A condição `if v < w` garante que cada aresta seja inserida uma única vez, resultando em `|E| = 168` e não em 336.

**2. Vetor `dist_to` acrescentado ao `BreadthFirstPaths`.** A implementação de referência mantém apenas `marked` e `edge_to`, suficientes para alcançabilidade e reconstrução de caminho, mas não para a contagem de movimentos. Foram acrescentadas três linhas: a criação do vetor, a inicialização `dist_to[s] = 0` e a atualização `dist_to[w] = dist_to[v] + 1` no momento da descoberta.

**3. Marcador de ausência.** A referência inicializa `edge_to` com `0`, valor que também é índice de vértice válido (casa `a1`). Ambos os vetores passaram a ser inicializados com `-1`, que não corresponde a nenhum vértice e funciona como marcador de ausência de predecessor e de distância infinita.

**4. Substituição do `Bag` por lista nativa.** A classe `Graph` da referência armazena a vizinhança em `Bag`, lista encadeada do algs4. Foi substituída por lista nativa do Python, que cumpre o mesmo papel. A estrutura de representação permanece a lista de adjacência.

**5. Leitura e formatação da saída.** Acrescentadas a função `le_casa()`, que converte a notação algébrica em índice, e o laço de leitura de `sys.stdin` até EOF, com impressão no formato exato exigido pelo enunciado.

### Integração

O grafo é construído **uma única vez**, antes da leitura de qualquer caso de teste, refletindo em código a representação implícita definida no Marco 2. A cada linha lida, uma nova BFS é executada a partir da casa de origem, e `dist_to[destino]` fornece a resposta. Um grafo, uma busca por consulta.

---

## 7. Testes

Teste local com o exemplo oficial do enunciado, por redirecionamento de `dados/casos-de-teste.txt`:

| Entrada | Saída obtida | Esperada |
| :------ | :----------: | :------: |
| `e2 e4` | 2 | 2 |
| `a1 b2` | 4 | 4 |
| `b2 c3` | 2 | 2 |
| `a1 h8` | 6 | 6 |
| `a1 h7` | 5 | 5 |
| `h8 a1` | 6 | 6 |
| `b1 c3` | 1 | 1 |
| `f6 f6` | 0 | 0 |

Verificações estruturais sobre o grafo construído:

- `|V| = 64` e `|E| = 168`, coerentes com o Marco 2;
- `degree(a1) = 2` e `degree(c3) = 8`, correspondendo ao grau mínimo e ao máximo previstos;
- nenhum valor `-1` remanescente em `dist_to` após a busca, confirmando que o grafo é conexo;
- `max(dist_to) = 6` a partir de `a1`, coerente com o diâmetro registrado no Marco 2.

Casos-limite verificados: origem igual ao destino (`f6 f6`, resultado 0); casas de canto (`a1`, `h8`, grau 2); simetria da consulta (`a1 h8` e `h8 a1` produzem o mesmo valor); e encerramento da leitura ao fim da entrada, sem contador prévio de casos.

---

## 8. Complexidade

| Etapa | Custo |
| :--- | :--- |
| Construção do grafo | `O(V + E)`, executada uma única vez |
| BFS por consulta | `O(V + E)` |
| Total para `Q` consultas | `O(V + E + Q·(V + E))` |

Com `V = 64` e `E = 168` constantes, o custo por consulta é limitado por uma constante, e o total cresce linearmente com o número de casos de teste.

---

## 9. Submissão

| Item | Registro |
| :--- | :--- |
| Plataforma | beecrowd |
| Problema | 1100 — Movimentos do Cavalo |
| Linguagem | Python 3.9 |
| Resultado | **Accepted** |
| Tempo de execução | 0,264 s (limite: 1 s) |
| Submissão | #49887578 — 03/09/2026 |
| Evidência | `evidencias/image.png` |

---

## 10. Ensaio

O trabalho mostrou que a etapa determinante não foi algorítmica, mas de modelagem. O enunciado do problema F é formulado inteiramente em termos de xadrez — um cavalo, um tabuleiro, um movimento em "L" — e não menciona grafos em momento algum. Foi preciso decidir o que seria vértice e o que seria aresta antes que qualquer conteúdo da disciplina se tornasse aplicável. Tomada essa decisão, o vocabulário do xadrez deixou de operar e restou uma pergunta conhecida: o menor número de arestas em um caminho entre dois vértices. A dificuldade inicial, que parecia estar na complexidade do problema, estava na tradução.

A comparação entre as duas buscas trouxe a distinção mais útil do trabalho: percorrer um grafo corretamente não é o mesmo que resolver o problema proposto. A DFS executa sem erro sobre a instância — alcança todos os vértices da componente, identifica o vértice isolado e detecta o ciclo pela aresta de retorno — e ainda assim entrega respostas erradas para a pergunta feita. O caso `0 → 7`, em que dois vértices adjacentes são ligados por um caminho de sete arestas, tornou isso concreto de um modo que nenhuma definição teria tornado. Um algoritmo pode estar correto quanto ao que faz e ser inadequado quanto ao que se pede dele.

Por fim, a solução aceita depende de uma condição que o enunciado não declara: todos os movimentos do cavalo custam o mesmo. É por o grafo ser não ponderado que contar arestas equivale a medir custo, e é apenas sob essa condição que a BFS garante o mínimo. Caso os movimentos tivessem custos distintos, seria necessário um algoritmo de caminho de custo mínimo. Delimitar o alcance da garantia mostrou-se tão relevante quanto obter o resultado aceito — saber por que a solução funciona é também saber quando ela deixaria de funcionar.
