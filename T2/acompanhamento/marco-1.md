# Marco 1 - Problema e Conhecimento Prévio: Paintball

## Histórico de Alterações

| Versão | Data       | Descrição da Alteração |
| :------ | :--------- | :--------------------- |
| 1.0     | 17/09/2026 | Criação do documento: resumo do problema, modelagem, classificaçã, papel da busca e instância pequena |

---

## Grupo A: Problema I (Paintball | Kattis)

**Link oficial:** <https://open.kattis.com/problems/paintball>

---

## 1. Entrada, Saída e Restrições

### Enunciado

`n` jogadores participam de uma partida de paintball. Alguns pares de jogadores **se enxergam mutuamente** — se um vê o outro, o outro também o vê.

Cada jogador deve **atirar em exatamente um** jogador que enxerga, e deve **receber exatamente um** tiro. O objetivo é determinar se essa organização é possível e, em caso afirmativo, exibi-la.

### Entrada

```text
n m
a b
a b
...
```

- primeira linha: `n` = número de jogadores, `m` = número de pares que se enxergam;
- as `m` linhas seguintes contêm dois inteiros `a` e `b`, indicando que os jogadores `a` e `b` se enxergam.

A relação de visão é **dada pela entrada e não pode ser alterada**. Ela é a restrição do problema; a decisão é apenas em quem cada jogador atira.

### Saída

Se a organização for possível, `n` linhas: a `i`-ésima linha contém o jogador em quem o jogador `i` atira.

Caso contrário, `Impossible`.

### Restrições

- a relação de visão é simétrica (não orientada);
- um jogador não atira em si mesmo;
- cada jogador atira **exatamente uma vez** e é atingido **exatamente uma vez**;
- a solução, quando existe, pode não ser única — qualquer organização válida é aceita.

---

## 2. Modelagem de Vértices e Arestas

### O grafo da entrada não é bipartido

A entrada descreve um grafo não orientado comum: vértice = jogador, aresta = "estes dois se enxergam". Não há bipartição natural.

### Construção da bipartição

Cada jogador desempenha **dois papéis independentes**: ele atira em alguém e é atingido por alguém — e essas duas escolhas não estão relacionadas entre si.

A modelagem explora isso **duplicando cada jogador em duas cópias**:

| Cópia | Papel |
| :--- | :--- |
| `i_atirador` | o jogador `i` como quem dispara |
| `i_alvo` | o jogador `i` como quem recebe o disparo |

O grafo modelado tem então:

- **vértices:** `2n` — `n` atiradores e `n` alvos;
- **arestas:** para cada par `a b` da entrada, duas arestas, pois a visão é mútua:

```text
a_atirador → b_alvo
b_atirador → a_alvo
```

Total: `2m` arestas.

Toda aresta liga um atirador a um alvo; nenhuma liga duas cópias do mesmo lado. **A bipartição é construída pela modelagem, não fornecida pelo enunciado.**

### O que o problema passa a pedir

Selecionar um subconjunto de arestas em que **cada atirador apareça exatamente uma vez e cada alvo apareça exatamente uma vez** — ou seja, um **emparelhamento perfeito** no grafo bipartido.

Se existir, ele descreve a organização pedida. Se não existir, a resposta é `Impossible`.

---

## 3. Classificação do Grafo

| | Grafo da entrada | Grafo modelado |
| :--- | :--- | :--- |
| Orientação | não orientado (visão mútua) | arestas orientadas logicamente do atirador para o alvo; como toda aresta cruza as partições, pode ser tratado como não orientado |
| Pesos | não ponderado | não ponderado |
| Laços e paralelas | simples | simples |
| Bipartição | não bipartido em geral | **bipartido por construção** |
| Conectividade | pode ser desconexo | pode ser desconexo |
| Ordem | `n` | `2n` |
| Tamanho | `m` | `2m` |

### Observação sobre conectividade

A conexidade **não determina** a existência de solução:

- um grafo **desconexo pode ter solução**: com `n = 4` e os pares `1–2` e `3–4`, cada componente se resolve internamente e todos os jogadores ficam atendidos;
- um grafo **conexo pode não ter solução**: com `n = 3` e os pares `1–2` e `2–3`, os jogadores `1` e `3` enxergam apenas o `2`, e ambos precisariam atirar nele — mas o `2` só pode receber um disparo.

O que determina a resposta é a existência do emparelhamento perfeito, não a conexidade.

Também vale notar que **ciclos ímpares não impedem a solução**: no triângulo `1–2–3`, a organização `1 → 2`, `2 → 3`, `3 → 1` é válida. A bipartição relevante é a do grafo construído, não a do grafo da entrada.

---

## 4. Resultado de Aprendizagem Aferido

**Emparelhamento em grafos bipartidos.**

O problema exige reconhecer que uma restrição de exclusividade mútua — cada elemento usado uma única vez de cada lado — corresponde a um emparelhamento, e que a bipartição pode ser obtida por desdobramento de papéis quando não está presente no enunciado.

Conceitos mobilizados: bipartição, emparelhamento, emparelhamento perfeito, caminho aumentante e percurso em grafo.

---

## 5. Participação de DFS/BFS na Solução

A busca não é a resposta do problema, como no T1: ela é a **ferramenta aplicada repetidamente** para construir o emparelhamento.

### Caminho aumentante

Partindo de um atirador ainda sem alvo, procura-se um **caminho alternado**: uma aresta fora do emparelhamento, depois uma dentro, depois uma fora, e assim por diante, até alcançar um alvo ainda não emparelhado.

Encontrado esse caminho, invertem-se as arestas ao longo dele — as que estavam no emparelhamento saem, as que estavam fora entram. O emparelhamento cresce em exatamente uma unidade.

**Exemplo.** Suponha que `1_atirador` já esteja emparelhado com `2_alvo`, e que `3_atirador` enxergue apenas o jogador `2`:

```text
3_atirador → 2_alvo → 1_atirador → 5_alvo (livre)
```

Invertendo: `1_atirador` passa a mirar `5_alvo` e `3_atirador` fica com `2_alvo`. Os dois ficam atendidos.

### Algoritmo

1. emparelhamento inicial vazio;
2. para cada atirador ainda sem alvo, executar uma busca procurando caminho aumentante;
3. se encontrar, inverter o caminho; se não encontrar, aquele atirador permanece sem par;
4. ao final, se os `n` atiradores estiverem emparelhados, existe emparelhamento perfeito.

### Escolha entre DFS e BFS

Adota-se **DFS**. O objetivo é apenas **encontrar algum** caminho aumentante, não o mais curto — logo a garantia de minimalidade da BFS não traz benefício. A DFS avança até alcançar um alvo livre ou esgotar as alternativas, comportamento que corresponde diretamente à busca por caminho alternado.

Custo: `O(V · E)`, uma busca por atirador não emparelhado.

Existe uma variante com BFS (Hopcroft–Karp) de custo `O(E√V)`, que será considerada apenas se a versão com DFS não atender ao limite de tempo.

### Estado adicional mantido pela busca

Além da marcação de visitados, a busca mantém o vetor de **correspondência** (para cada alvo, qual atirador o tem no momento), que é o que permite continuar o caminho alternado ao chegar em um alvo já ocupado. A formalização desse estado será feita no Marco 2.

---

## 6. Instância Pequena

### Caso positivo

```text
Entrada:        Saída:
2 1             2
1 2             1
```

Dois jogadores que se enxergam. Grafo modelado:

```text
ATIRADORES        ALVOS

    1  ──────────▶  2
    2  ──────────▶  1
```

As duas arestas formam o emparelhamento perfeito: o jogador `1` atira no `2` e o jogador `2` atira no `1`.

### Caso negativo — vértice isolado

```text
Entrada:        Saída:
3 1             Impossible
1 2
```

O jogador `3` não enxerga ninguém: a cópia `3_atirador` não possui aresta alguma e nunca pode ser emparelhada.

### Caso negativo — disputa pelo mesmo alvo

```text
Entrada:        Saída:
3 2             Impossible
1 2
2 3
```

Os jogadores `1` e `3` enxergam somente o `2`. Ambos precisariam atirar nele, mas `2_alvo` só admite um atirador. O grafo da entrada é **conexo** e ainda assim não há solução.

### Caso-limite — desconexo com solução

```text
Entrada:        Saída:
4 2             2
1 2             1
3 4             4
                3
```

Duas componentes independentes, cada uma resolvida internamente. Confirma que desconexão não implica `Impossible`.
