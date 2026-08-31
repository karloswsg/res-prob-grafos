# Marco 3 - Aplicação Básica de DFS: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 27/08/2026 | Criação do documento: execução manual da DFS na instância 3×3, estados de visita, tempos, árvore de busca, alcançabilidade e análise de aplicabilidade |
| 1.1     | 27/08/2026 | Padronização dos estados de visita para a marcação booleana `marked[]` |
| 1.2     | 30/08/2026 | Substituição do contador único de tempos pelas posições de pré-ordem e pós-ordem, inclusão da verificação `d[v] + f[v] = 9` e da ressalva sobre árvores ramificadas |

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

Cada linha é um passo da execução. Dois tipos de evento: **descoberta** (o vértice é visitado e marcado) e **término** (a recursão retorna dele, com todos os vizinhos verificados). Cada tipo de evento é numerado na sua própria sequência: as descobertas geram a pré-ordem, os términos geram a pós-ordem.

| Passo | Evento     | Vértice | Ordem   | Pilha de recursão     | Observação                          |
| :---: | :--------- | :-----: | :-----: | :-------------------- | :---------------------------------- |
| 1     | descoberta | 0       | pré 1   | `0`                   | origem                              |
| 2     | descoberta | 5       | pré 2   | `0 5`                 | 1º vizinho de `0`                   |
| 3     | descoberta | 6       | pré 3   | `0 5 6`               | `0` já marcado, ignorado            |
| 4     | descoberta | 1       | pré 4   | `0 5 6 1`             | 1º vizinho de `6`                   |
| 5     | descoberta | 8       | pré 5   | `0 5 6 1 8`           | `6` já marcado, ignorado            |
| 6     | descoberta | 3       | pré 6   | `0 5 6 1 8 3`         | `1` já marcado, ignorado            |
| 7     | descoberta | 2       | pré 7   | `0 5 6 1 8 3 2`       | 1º vizinho de `3`                   |
| 8     | descoberta | 7       | pré 8   | `0 5 6 1 8 3 2 7`     | `3` já marcado, ignorado            |
| 9     | término    | 7       | pós 1   | `0 5 6 1 8 3 2`       | vizinhos `0` e `2` já marcados      |
| 10    | término    | 2       | pós 2   | `0 5 6 1 8 3`         | vizinhos esgotados                  |
| 11    | término    | 3       | pós 3   | `0 5 6 1 8`           | vizinhos esgotados                  |
| 12    | término    | 8       | pós 4   | `0 5 6 1`             | vizinhos esgotados                  |
| 13    | término    | 1       | pós 5   | `0 5 6`               | vizinhos esgotados                  |
| 14    | término    | 6       | pós 6   | `0 5`                 | vizinhos esgotados                  |
| 15    | término    | 5       | pós 7   | `0`                   | vizinhos esgotados                  |
| 16    | término    | 0       | pós 8   | `—`                   | `7` já marcado; busca encerrada     |

Como o grafo é um ciclo, cada vértice possui exatamente um vizinho ainda não descoberto no momento da visita. A busca mergulha em sequência única (8 descobertas consecutivas) e só então retrocede (8 términos consecutivos).

---

## 3. Estados de Visita, Tempos e Predecessores

Cada vértice possui um estado de visita registrado na marcação booleana `marked[v]`: **`true`** se o vértice foi visitado durante a busca, **`false`** caso contrário.

`d[v]` e `f[v]` registram a posição do vértice em cada uma das duas ordenações produzidas pela busca: `d[v]` é a posição na **pré-ordem**, a sequência em que os vértices são alcançados; `f[v]` é a posição na **pós-ordem**, a sequência em que são concluídos. Cada ordenação numera os 8 vértices alcançados de 1 a 8.

| Vértice | `marked[v]` | `d[v]` (pré-ordem) | `f[v]` (pós-ordem) | Predecessor `edgeTo[v]` |
| :-----: | :---------- | :----------------: | :----------------: | :---------------------: |
| 0       | `true`      | 1                  | 8                  | — (origem)              |
| 5       | `true`      | 2                  | 7                  | 0                       |
| 6       | `true`      | 3                  | 6                  | 5                       |
| 1       | `true`      | 4                  | 5                  | 6                       |
| 8       | `true`      | 5                  | 4                  | 1                       |
| 3       | `true`      | 6                  | 3                  | 8                       |
| 2       | `true`      | 7                  | 2                  | 3                       |
| 7       | `true`      | 8                  | 1                  | 2                       |
| **4**   | **`false`** | —                  | —                  | —                       |

As duas ordenações completas:

```
pré-ordem  (por d[v]):   0  5  6  1  8  3  2  7
pós-ordem  (por f[v]):   7  2  3  8  1  6  5  0
```

**Verificação.** Nesta instância vale `d[v] + f[v] = 9` para todos os oito vértices alcançados. A identidade decorre de a pós-ordem ser exatamente o inverso da pré-ordem: o `k`-ésimo vértice alcançado é o `(9 − k)`-ésimo a concluir. Qualquer erro no rastreio quebraria a soma em alguma linha.

**Ressalva.** A simetria entre as duas ordenações decorre da forma da árvore de busca, que aqui é um caminho sem ramificação: a busca desce em sequência única e retorna desfazendo na ordem contrária. Em uma árvore que ramifique, as ordenações não são simétricas — um vértice de um ramo posterior é concluído somente após todo o ramo anterior, ainda que tenha sido alcançado depois dele.

Independentemente do formato da árvore, a origem ocupa sempre a última posição da pós-ordem, pois sua chamada só retorna quando todas as chamadas aninhadas já retornaram. É o que se observa em `f[0] = 8`. Simetricamente, o vértice `7` ocupa a última posição da pré-ordem e a primeira da pós-ordem: foi o último a ser alcançado e o primeiro a concluir, por estar no fundo do mergulho e ter ambos os vizinhos já marcados.

---

## 4. Árvore de Busca

Reconstruída a partir dos predecessores:

```
0 → 5 → 6 → 1 → 8 → 3 → 2 → 7
```

- 8 vértices alcançados, **7 arestas** na árvore (`V − 1`).
- O grafo possui 8 arestas; portanto **1 aresta ficou fora**: a aresta `0–7`.

A aresta `0–7` foi encontrada no tempo 8 (a partir de `7`, ao verificar `0`) e descartada, pois `0` já estava marcado e ainda na pilha de recursão. Aresta que aponta para um vértice ainda na pilha é uma **aresta de retorno**, e evidencia a existência de um ciclo no grafo — o que confirma que o grafo do cavalo não é acíclico.

---

## 5. Alcançabilidade

O vértice `4` permanece **não marcado** (`marked[4] = false`) ao final da busca: nenhuma aresta incide sobre ele, pois todos os 8 saltos do cavalo a partir do centro do 3×3 caem fora do tabuleiro.

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
