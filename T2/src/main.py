"""
Hopcroft-Karp traduzido de algs4-java/HopcroftKarp.java

Modelagem:
  cada jogador vira DUAS copias, pois exerce dois papeis independentes:
    atirador i -> vertice  i        (lado L, cor True)
    alvo     j -> vertice  n + j    (lado R, cor False)
  cada par de visao "a b" gera DUAS arestas, pois a visao e mutua:
    a_atirador -- b_alvo     e     b_atirador -- a_alvo
  nunca existe aresta i -- n+i: um jogador nao atira em si mesmo.

Relacao com fluxo:
  toda aresta tem capacidade 1. Aresta emparelhada esta SATURADA;
  aresta nao emparelhada tem RESIDUO. is_residual_graph_edge testa isso.
"""

import sys
from collections import deque


# =============================================================================
# BLOCO 1 - GRAFO (equivale a algs4.Graph)
# =============================================================================

class Graph:
    """Grafo nao orientado por lista de adjacencia."""

    def __init__(self, V):
        self.V = V
        self.E = 0
        self._adj = [[] for _ in range(V)]

    def add_edge(self, v, w):
        self._adj[v].append(w)
        self._adj[w].append(v)      # nao orientado: entra nas duas listas
        self.E += 1

    def adj(self, v):
        return self._adj[v]


# =============================================================================
# BLOCO 2 - CONSTRUCAO DO GRAFO BIPARTIDO (desdobramento dos papeis)
# =============================================================================

def constroi_grafo_bipartido(n, pares):
    """Monta o grafo com 2n vertices a partir dos pares de visao.

    indices  0 .. n-1    -> atiradores (lado L)
    indices  n .. 2n-1   -> alvos      (lado R)
    """
    G = Graph(2 * n)
    for a, b in pares:
        # a enxerga b, logo a pode atirar em b
        if a != b:                      # restricao: ninguem atira em si mesmo
            G.add_edge(a, n + b)
        # a visao e mutua, logo b tambem pode atirar em a
        if b != a:
            G.add_edge(b, n + a)
    return G


# =============================================================================
# BLOCO 3 - BIPARTICAO (substitui algs4.BipartiteX)
# =============================================================================

class Biparticao:
    """Cor de cada vertice.

    A referencia usa BipartiteX para DETECTAR a biparticao procurando
    ciclo impar. Aqui a biparticao e CONSTRUIDA pelo desdobramento:
    todo vertice < n e atirador, todo vertice >= n e alvo.
    A deteccao e desnecessaria porque a bipartição ja e conhecida.
    """

    def __init__(self, n):
        self.n = n

    def color(self, v):
        """True  = atirador (lado L, onde as buscas comecam)
           False = alvo     (lado R)"""
        return v < self.n


# =============================================================================
# BLOCO 4 - HOPCROFT-KARP
# =============================================================================

class HopcroftKarp:
    """Emparelhamento maximo em grafo bipartido, por fases."""

    UNMATCHED = -1
    INFINITY = float('inf')

    def __init__(self, G, biparticao):
        self.G = G
        self.bipartition = biparticao
        self.V = G.V
        self.cardinality = 0

        # mate[v] = w  se a aresta v-w esta no emparelhamento
        # mate[v] = -1 se v nao esta emparelhado
        self.mate = [self.UNMATCHED] * self.V

        self.marked = None      # marked[v] = v e alcancavel por caminho alternante
        self.dist_to = None     # dist_to[v] = nivel de v no grafo de niveis

        # ---------------------------------------------------------------
        # LACO DE FASES
        # enquanto a BFS disser que ainda existe caminho aumentante,
        # a DFS colhe varios caminhos minimos disjuntos naquela fase.
        # ---------------------------------------------------------------
        while self._has_augmenting_path():

            # proximo[v] guarda qual vizinho de v ainda nao foi testado.
            # A versao recursiva fazia isso sozinha, no "for".
            # Com pilha explicita, e preciso guardar a posicao a mao.
            proximo = [0] * self.V

            for s in range(self.V):
                # so inicia por atirador (cor True) ainda nao emparelhado
                if self._is_matched(s) or not self.bipartition.color(s):
                    continue

                # -------------------------------------------------------
                # DFS NAO RECURSIVA, com o caminho visivel na pilha
                # -------------------------------------------------------
                path = [s]
                while path:
                    v = path[-1]                     # topo, sem retirar

                    if proximo[v] >= len(self.G.adj(v)):
                        path.pop()                   # RECUA: acabaram os vizinhos
                        continue

                    w = self.G.adj(v)[proximo[v]]
                    proximo[v] += 1

                    if not self._is_level_graph_edge(v, w):
                        continue                     # aresta fora do grafo de niveis

                    path.append(w)                   # AVANCA

                    if not self._is_matched(w):
                        # CAMINHO AUMENTANTE ENCONTRADO.
                        # Neste ponto, "path" contem o caminho inteiro.
                        # Inverter = percorrer a pilha em pares e trocar os mates.
                        while path:
                            x = path.pop()
                            y = path.pop()
                            self.mate[x] = y
                            self.mate[y] = x
                        self.cardinality += 1

    # -------------------------------------------------------------------
    # BLOCO 4.1 - RESIDUO (o conceito de fluxo dentro do algoritmo)
    # -------------------------------------------------------------------
    def _is_residual_graph_edge(self, v, w):
        """A aresta v-w pode ser atravessada no sentido v -> w?

        Capacidade de toda aresta e 1.
          - do lado ATIRADOR (color True) so se atravessa aresta NAO emparelhada:
            ela ainda tem residuo.
          - do lado ALVO (color False) so se atravessa aresta EMPARELHADA:
            e o retorno pelo fluxo ja enviado.
        E isso que faz o caminho ALTERNAR entre arestas fora e dentro de M.
        """
        if self.mate[v] != w and self.bipartition.color(v):
            return True
        if self.mate[v] == w and not self.bipartition.color(v):
            return True
        return False

    # -------------------------------------------------------------------
    # BLOCO 4.2 - GRAFO DE NIVEIS
    # -------------------------------------------------------------------
    def _is_level_graph_edge(self, v, w):
        """A aresta v-w avanca exatamente um nivel E tem residuo?

        E o que obriga a DFS a andar SO PARA FRENTE, garantindo que os
        caminhos encontrados sejam os MINIMOS daquela fase.
        """
        return self.dist_to[w] == self.dist_to[v] + 1 and self._is_residual_graph_edge(v, w)

    # -------------------------------------------------------------------
    # BLOCO 4.3 - BFS: MEDE os niveis, nao encontra caminho
    # -------------------------------------------------------------------
    def _has_augmenting_path(self):
        """BFS a partir de TODOS os atiradores livres ao mesmo tempo.

        Responde duas coisas:
          1. ainda existe caminho aumentante?
          2. qual o nivel de cada vertice?
        Nao encontra nenhum caminho: isso e tarefa da DFS.
        """
        self.marked = [False] * self.V
        self.dist_to = [self.INFINITY] * self.V

        fila = deque()
        for v in range(self.V):
            if self.bipartition.color(v) and not self._is_matched(v):
                fila.append(v)
                self.marked[v] = True
                self.dist_to[v] = 0

        achou = False
        while fila:
            v = fila.popleft()
            for w in self.G.adj(v):
                if self._is_residual_graph_edge(v, w):
                    if not self.marked[w]:
                        self.dist_to[w] = self.dist_to[v] + 1
                        self.marked[w] = True
                        if not self._is_matched(w):
                            achou = True
                        # para de enfileirar depois de achar um alvo livre:
                        # nenhum caminho mais longo interessa nesta fase
                        if not achou:
                            fila.append(w)
        return achou

    # -------------------------------------------------------------------
    # BLOCO 4.4 - CONSULTAS
    # -------------------------------------------------------------------
    def _is_matched(self, v):
        return self.mate[v] != self.UNMATCHED

    def size(self):
        return self.cardinality

    def is_perfect(self):
        """Na referencia: cardinality == min(V1, V2).
        Aqui os dois lados tem tamanho n, logo basta comparar com n."""
        return self.cardinality == self.bipartition.n


# =============================================================================
# BLOCO 5 - LEITURA E SAIDA
# =============================================================================

def main():
    dados = sys.stdin.buffer.read().split()
    n = int(dados[0])
    m = int(dados[1])

    pares = []
    for k in range(m):
        a = int(dados[2 + 2 * k]) - 1       # entrada e 1..n, vetores sao 0..n-1
        b = int(dados[3 + 2 * k]) - 1
        pares.append((a, b))

    G = constroi_grafo_bipartido(n, pares)
    hk = HopcroftKarp(G, Biparticao(n))

    if not hk.is_perfect():
        sys.stdout.write("Impossible\n")
    else:
        # mate[i] guarda o vertice do ALVO, que vale n + jogador.
        # Subtrai n para voltar ao numero do jogador, e soma 1 para a saida.
        saida = "\n".join(str(hk.mate[i] - n + 1) for i in range(n))
        sys.stdout.write(saida + "\n")


if __name__ == "__main__":
    main()
