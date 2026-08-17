# Marco 1 - Modelagem: O Problema do Movimento do Cavalo

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

| Origem | Destino | Resultado Esperado                             | Observação do Teste    |
| :----- | :------ | :--------------------------------------------- | :----------------------- |
| e2     | e4      | `To get from e2 to e4 takes 2 knight moves.` | Instância curta padrão |
| a1     | h8      | `To get from a1 to h8 takes 6 knight moves.` | Extremos opostos         |
| f6     | f6      | `To get from f6 to f6 takes 0 knight moves.` | Custo Zero               |

## 4. Hipótese Inicial de Solução

A abordagem mais eficiente para garantir o caminho ótimo neste cenário é a implementação do algoritmo de **Busca em Largura (BFS - Breadth-First Search)**.

A execução utilizará uma estrutura de dados do tipo fila (Queue) para explorar os vértices adjacentes em camadas de distância. A partir da coordenada inicial, o algoritmo mapeia todos os movimentos válidos, adicionando-os ao final da fila e registrando essas casas em um conjunto (Set) de vértices visitados para evitar ciclos infinitos. A busca avança iterativamente, somando +1 ao custo a cada nova camada de expansão da onda. A execução é interrompida imediatamente assim que o vértice de destino for encontrado na fila, o que garante matematicamente a descoberta da rota com o menor número de saltos possível, sem a necessidade de explorar rotas ineficientes.
