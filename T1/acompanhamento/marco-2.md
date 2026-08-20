# Marco 2 - Representação Computacional: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :------------------------- |
| 1.0     | 20/08/2026 | Criação do documento     |

## 1. Representação Computacional Escolhida

Para um grafo com 64 vértices fixos e regras de adjacência bem definidas (o "L" do cavalo), três representações clássicas poderiam ser adotadas: **matriz de adjacência**, **lista de adjacência** e **representação implícita**.

* **Matriz de adjacência (64×64):** consumiria 4096 posições, das quais apenas 336 (duas vezes o número de arestas) seriam preenchidas com 1. Como a densidade do grafo é baixa, a matriz seria majoritariamente composta por zeros, desperdiçando memória sem trazer ganho algum.
* **Lista de adjacência:** representaria cada vértice com um vetor contendo apenas seus vizinhos reais, sendo mais eficiente em memória que a matriz. É uma opção válida, mas exige a etapa extra de pré-computar e armazenar as listas para os 64 vértices.
* **Representação implícita (escolhida):** como as regras de movimento do cavalo são fixas e idênticas para qualquer casa do tabuleiro, os vizinhos de um vértice `(coluna, linha)` podem ser calculados **sob demanda**, aplicando os 8 deslocamentos possíveis `(±1, ±2)` e `(±2, ±1)` e descartando os que caem fora dos limites `1..8`.

**Justificativa da escolha:** a representação implícita é a mais adequada para este problema porque evita gasto de memória com uma matriz esparsa, elimina a etapa de pré-processamento de listas de adjacência, já que os vizinhos são triviais de calcular a partir de uma fórmula fixa, sendo a abordagem natural quando o grafo é gerado por uma regra determinística (o padrão de salto do cavalo), em vez de por uma lista arbitrária de arestas fornecida na entrada.

## 2. Leitura da Entrada e Construção do Grafo

### 2.1 Leitura da Entrada

Cada linha da entrada contém duas strings (ex.: `e2 e4`), lidas até o fim do arquivo, pois o problema não informa previamente a quantidade de casos de teste. Cada string é decomposta em:

* **Coluna:** um caractere `'a'`–`'h'`, convertido para um índice numérico `0`–`7` (ex.: `coluna - 'a'`).
* **Linha:** um dígito `'1'`–`'8'`, convertido para inteiro.

### 2.2 Construção do Grafo (Geração de Vizinhos)

A função de vizinhança `vizinhos(coluna, linha)` aplica os 8 deslocamentos possíveis do cavalo:

```
deslocamentos = [(1,2), (2,1), (2,-1), (1,-2),
                  (-1,-2), (-2,-1), (-2,1), (-1,2)]
```

Para cada deslocamento `(dc, dl)`, calcula-se a nova posição `(coluna+dc, linha+dl)` e valida-se se `0 ≤ coluna+dc ≤ 7` e `1 ≤ linha+dl ≤ 8`. Somente posições válidas são retornadas como vizinhas. Essa função é chamada a cada expansão de vértice durante a BFS, construindo o grafo "sob demanda" e não como uma estrutura persistida em memória.

## 3. Medidas Estruturais Pertinentes

As medidas abaixo foram calculadas computacionalmente a partir da geração de vizinhos descrita na Seção 2, percorrendo os 64 vértices do tabuleiro:

| Medida                                | Valor                                      |
| :------------------------------------ | :----------------------------------------- |
| **Ordem**                       | 64                                         |
| **Tamanho**                     | 168                                        |
| **Grau mínimo**                | 2                                          |
| **Grau máximo**                | 8                                          |
| **Densidade** (2·E / V·(V-1)) | ≈ 0,083                                   |
| **Conectividade**               | Conexo                                     |
| **Bipartição**                | Alternância entre casas claras e escuras) |
| **Diâmetro**                  | 6                                          |
