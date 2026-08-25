# Marco 1 - Modelagem: O Problema do Movimento do Cavalo

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :------------------------- |
| 1.0     | 17/08/2026 | Criação do documento     |
| 1.1    | 25/08/2026 | Ajuste no ponto 3 para uso de um tabuleiro 3x3 como instância pequena; ajuste no ponto 4 considerando o uso de lista de adjacência para a resolução |
---

## Grupo A: Problema F (Movimentos do Cavalo | Beecrowd 1100)

| Integrante                     | Matrícula |
| ------------------------------ | ---------- |
| Karlos Eduardo Sousa Pinto     | 2320262    |
| Maria Eduarda Coutinho Angelim | 2324319    |

---

## 1. Definições

* **Enunciado:** O objetivo é desenvolver um programa que calcule o menor número de movimentos necessários para um cavalo de xadrez se deslocar de um quadrado de origem `a` até um quadrado de destino `b` em um tabuleiro padrão.
* **Entrada:** A leitura consiste em múltiplos casos de teste. Cada caso é uma linha contendo duas strings separadas por espaço (exemplo: `e2 e4`), representando as posições de origem e destino. As colunas são letras de `a` a `h` e as linhas são dígitos de `1` a `8`.
* **Saída:** A aplicação deve imprimir uma frase exata para cada caso de teste no formato: `To get from xx to yy takes n knight moves.`, onde `xx` é a origem, `yy` é o destino e `n` é a quantidade mínima de movimentos calculada.
* **Restrições:** O cavalo move-se exclusivamente em "L" (duas casas em um eixo, uma no eixo perpendicular). É estritamente proibido que qualquer salto resulte em uma coordenada fora dos limites da matriz 8x8. O processamento deve lidar com múltiplas entradas sequenciais.

## 2. Mapeamento da Modelagem

* **Vértices:** O grafo possui 64 vértices fixos, correspondendo a cada uma das posições únicas do tabuleiro (de `a1` a `h8`).
* **Arestas:** Cada aresta representa um salto válido do cavalo entre dois vértices do tabuleiro. Todas as arestas possuem peso/custo igual a 1, já que o objetivo é apenas contar a quantidade de saltos.
* **Tipo do Grafo:** Trata-se de um grafo não direcionado (se o cavalo vai de A para B, ele pode voltar de B para A), não ponderado, conexo (todas as casas são alcançáveis) e bipartido (os saltos sempre alternam entre casas claras e escuras).

## 3. Instância Pequena

Para validar manualmente a lógica de movimentação do cavalo antes de aplicá-la ao tabuleiro 8x8 completo, foi utilizada uma instância reduzida: um tabuleiro **3x3**, com as 9 casas numeradas sequencialmente de `0` a `8` (linha a linha, da esquerda para a direita), conforme o diagrama abaixo:

```
 0 | 1 | 2
-----------
 3 | 4 | 5
-----------
 6 | 7 | 8
```

Aplicando as 8 possibilidades de salto do cavalo a cada casa e descartando os saltos que caem fora do tabuleiro, obtém-se a seguinte lista de adjacência (vizinhos válidos de cada vértice):

| Vértice | Vizinhos |
| :------: | :------- |
|    0    | 5, 7     |
|    1    | 6, 8     |
|    2    | 3, 7     |
|    3    | 2, 8     |
|    4    |          |
|    5    | 0, 6     |
|    6    | 1, 5     |
|    7    | 0, 2     |
|    8    | 1, 3     |

Um resultado importante desta instância reduzida é que o vértice `4` (casa central) possui **grau 0**: em um tabuleiro 3x3 não existe nenhum salto de cavalo válido a partir do centro. Isso divide o grafo em **duas componentes conexas**: uma componente com os 8 vértices restantes (`{0,1,2,3,5,6,7,8}`), internamente conexa (existe caminho entre qualquer par deles), e uma componente trivial formada apenas pelo vértice `{4}`, sem nenhuma aresta ligando-o às demais casas. Como não há caminho entre essas duas componentes, o grafo da instância pequena como um todo é classificado como **desconexo** (diferente do tabuleiro 8x8, que é conexo, conforme a Seção 2) — sendo um caso útil justamente para testar como o algoritmo deve se comportar quando não existe caminho entre origem e destino.

| Origem | Destino | Resultado Esperado        | Observação do Teste                                                                                      |
| :----- | :------ | :------------------------ | :--------------------------------------------------------------------------------------------------------- |
| 6      | 8       | 2 movimentos              | Instância curta padrão                                                                                   |
| 0      | 8       | 4 movimentos              | Extremos opostos                                                                                           |
| 0      | 0       | 0 movimentos              | Custo zero                                                                                                 |
| 0      | 4       | Sem caminho (inexistente) | Vértice`4` forma uma componente conexa própria (grau 0), separada da componente dos outros 8 vértices |

## 4. Hipótese Inicial de Solução

Como o tabuleiro é fixo em 8×8, o grafo possui `|V| = 64` vértices e `|E| = 168` arestas (ambos conhecidos antecipadamente, sem depender da entrada), a hipótese de solução consiste em:

1. **Converter as coordenadas** de cada casa (ex.: `e2`) para um índice único `id = linha*8 + coluna`, viabilizando a representação do grafo em memória.
2. **Construir a lista de adjacência** uma única vez, aplicando os 8 deslocamentos possíveis do cavalo (`±1,±2` e `±2,±1`) a cada uma das 64 casas e descartando os saltos que caem fora do tabuleiro.
3. **Menor Caminho:** para cada caso de teste (origem, destino), executar uma Busca em Largura (BFS) a partir do vértice de origem, identificando e registrando a menor distância até o vértice de destino.
4. **Retorno:** formatar a saída exata `To get from xx to yy takes n knight moves.`, onde `n` é a distância mínima encontrada pelo BFS.

**Complexidade esperada da solução principal:** `O(V + E)` por caso de teste, com `V = 64` e `E = 168` fixos — portanto `O(1)` por consulta na prática, e `O(T·(V+E))` no total, onde `T` é o número de casos de teste lidos da entrada.
