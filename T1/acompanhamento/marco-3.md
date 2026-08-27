# Marco 3 - Aplicação Básica de DFS: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 27/08/2026 | Criação do documento: execução manual da DFS na instância 3×3, estados de visita, tempos, árvore de busca, alcançabilidade e análise de aplicabilidade |

---

## 1. Instância e Ponto de Partida

Instância: **tabuleiro 3×3**, a mesma dos Marcos 1 e 2, com as 9 casas numeradas de `0` a `8`, linha a linha.

Lista de adjacência (a ordem dos vizinhos determina o resultado da DFS):

| Vértice | Vizinhos |     | Vértice | Vizinhos |
| :-----: | :------- | :-: | :-----: | :------- |
| 0       | 5, 7     |     | 5       | 0, 6     |
| 1       | 6, 8     |     | 6       | 1, 5     |
| 2       | 3, 7     |     | 7       | 0, 2     |
| 3       | 2, 8     |     | 8       | 1, 3     |
| 4       | (vazia)  |     |         |          |

Origem da busca: vértice **0**.

---

## 2. Execução Manual

Cada linha é um passo do relógio. Dois tipos de evento: **descoberta** (o vértice entra em exploração) e **término** (o vértice conclui).

| t  | Evento     | Vértice | Pilha (em exploração) | Observação                                   |
| :-: | :--------- | :-----: | :-------------------- | :------------------------------------------- |
| 1  | descoberta | 0       | `0`                   | origem                                       |
| 2  | descoberta | 5       | `0 5`                 | 1º vizinho de `0`                            |
| 3  | descoberta | 6       | `0 5 6`               | `0` já em exploração, ignorado               |
| 4  | descoberta | 1       | `0 5 6 1`             | 1º vizinho de `6`                            |
| 5  | descoberta | 8       | `0 5 6 1 8`           | `6` já em exploração, ignorado               |
| 6  | descoberta | 3       | `0 5 6 1 8 3`         | `1` já em exploração, ignorado               |
| 7  | descoberta | 2       | `0 5 6 1 8 3 2`       | 1º vizinho de `3`                            |
| 8  | descoberta | 7       | `0 5 6 1 8 3 2 7`     | `3` já em exploração, ignorado               |
| 9  | término    | 7       | `0 5 6 1 8 3 2`       | vizinhos `0` e `2` já em exploração          |
| 10 | término    | 2       | `0 5 6 1 8 3`         | vizinhos esgotados                           |
| 11 | término    | 3       | `0 5 6 1 8`           | vizinhos esgotados                           |
| 12 | término    | 8       | `0 5 6 1`             | vizinhos esgotados                           |
| 13 | término    | 1       | `0 5 6`               | vizinhos esgotados                           |
| 14 | término    | 6       | `0 5`                 | vizinhos esgotados                           |
| 15 | término    | 5       | `0`                   | vizinhos esgotados                           |
| 16 | término    | 0       | `—`                   | `7` já concluído; busca encerrada            |

Como o grafo é um ciclo, cada vértice possui exatamente um vizinho ainda não descoberto no momento da visita. A busca mergulha em sequência única (8 descobertas consecutivas) e só então retrocede (8 términos consecutivos).

---

## 3. Estados de Visita, Tempos e Predecessores

Cada vértice percorre três estados: **não visitado** → **em exploração** → **concluído** (equivalentes às marcações branco/cinza/preto). Um vértice em exploração é um vértice que permanece na pilha de recursão.

| Vértice | Estado final  | `d[v]` (descoberta) | `f[v]` (término) | Predecessor `edgeTo[v]` |
| :-----: | :------------ | :-----------------: | :--------------: | :---------------------: |
| 0       | concluído     | 1                   | 16               | — (origem)              |
| 5       | concluído     | 2                   | 15               | 0                       |
| 6       | concluído     | 3                   | 14               | 5                       |
| 1       | concluído     | 4                   | 13               | 6                       |
| 8       | concluído     | 5                   | 12               | 1                       |
| 3       | concluído     | 6                   | 11               | 8                       |
| 2       | concluído     | 7                   | 10               | 3                       |
| 7       | concluído     | 8                   | 9                | 2                       |
| **4**   | **não visitado** | —                | —                | —                       |

Verificação: 8 vértices alcançados × 2 eventos = 16 tempos, distintos e no intervalo `1..16`. Em todos, `d[v] < f[v]`.

**Aninhamento dos intervalos.** Os intervalos `[d[v], f[v]]` são todos aninhados, sem cruzamento. O aninhamento é visível na coluna *Pilha (em exploração)* da Seção 2: os vértices concluem na ordem inversa à de descoberta, consequência direta da pilha de recursão. O intervalo de `0` (`[1,16]`) contém todos os demais, confirmando que `0` é a raiz da árvore de busca.

---

## 4. Árvore de Busca

Reconstruída a partir dos predecessores:

```
0 → 5 → 6 → 1 → 8 → 3 → 2 → 7
```

- 8 vértices alcançados, **7 arestas** na árvore (`V − 1`).
- O grafo possui 8 arestas; portanto **1 aresta ficou fora**: a aresta `0–7`.

A aresta `0–7` foi encontrada no tempo 8 (a partir de `7`, ao verificar `0`) e descartada, pois `0` estava em exploração. Aresta que aponta para um vértice ainda em exploração é uma **aresta de retorno**, e evidencia a existência de um ciclo no grafo — o que confirma que o grafo do cavalo não é acíclico.

---

## 5. Alcançabilidade

O vértice `4` permanece **não visitado** ao final da busca: nenhuma aresta incide sobre ele, pois todos os 8 saltos do cavalo a partir do centro do 3×3 caem fora do tabuleiro.

A DFS responde corretamente, portanto, à pergunta *"existe caminho entre dois vértices?"*:

| Consulta | Resposta da DFS       |
| :------- | :-------------------- |
| 0 → 8    | existe caminho        |
| 0 → 4    | **não existe caminho** |

Componentes conexas identificadas: `{0,1,2,3,5,6,7,8}` e `{4}` — o grafo da instância é desconexo, conforme registrado no Marco 1.

---

## 6. Aplicabilidade ao Problema

O problema F exige o **menor** número de movimentos. Comparando os caminhos produzidos pela árvore da DFS com as distâncias reais:

| Consulta | Caminho na árvore da DFS | Movimentos (DFS) | Distância real | Confere? |
| :------- | :----------------------- | :--------------: | :------------: | :------: |
| 0 → 7    | `0-5-6-1-8-3-2-7`        | 7                | 1              | não      |
| 0 → 2    | `0-5-6-1-8-3-2`          | 6                | 2              | não      |
| 0 → 8    | `0-5-6-1-8`              | 4                | 4              | sim      |
| 0 → 4    | inexistente              | —                | inexistente    | sim      |

O caso `0 → 7` é o mais evidente: `7` é vizinho direto de `0` (1 movimento), mas a DFS percorreu 7 arestas até alcançá-lo, porque escolheu `5` como primeiro vizinho e mergulhou até esgotar o ramo.

**Conclusão: a DFS não é aplicável para resolver o problema F.**

Justificativa: a DFS não visita os vértices em ordem crescente de distância a partir da origem. O primeiro caminho que ela encontra até um vértice é o caminho do mergulho corrente, cujo comprimento não tem relação com a distância mínima. A coincidência observada em `0 → 8` é acidental, não garantida.

Adicionalmente, o resultado da DFS **depende da ordem dos vizinhos** na lista de adjacência: invertendo a ordem de `adj[0]` para `7, 5`, o caminho até `7` passaria a ter 1 aresta. Um algoritmo cujo resultado varia com a ordem de armazenamento não pode garantir minimalidade.

---

## 7. Adaptação Parcial Pertinente

Ainda que não resolva o problema, a DFS fornece resultados aproveitáveis:

| Uso | Aplicação neste problema |
| :--- | :--- |
| Alcançabilidade (`marked[]`) | Confirma que o tabuleiro 8×8 é conexo — todas as 64 casas são alcançáveis de qualquer origem, logo nenhuma consulta fica sem resposta |
| Componentes conexas | Identifica o vértice isolado `4` na instância 3×3 |
| Detecção de ciclo | A aresta de retorno `7 → 0` comprova que o grafo possui ciclos |
| Reconstrução de caminho (`edgeTo[]`) | Recupera *um* caminho válido entre duas casas, útil caso o problema exigisse exibir a sequência de movimentos |
