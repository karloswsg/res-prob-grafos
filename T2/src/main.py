import sys
from collections import deque


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


def build_bipartite_graph(n, pairs):
    """Monta o grafo com 2n vertices a partir dos pares de visao.

    indices  0 .. n-1    -> atiradores (lado L)
    indices  n .. 2n-1   -> alvos      (lado R)
    """
    G = Graph(2 * n)
    for a, b in pairs:
        if a != b:
            G.add_edge(a, n + b)
        if b != a:
            G.add_edge(b, n + a)
    return G


class Bipartition:
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


class HopcroftKarp:
    """Emparelhamento maximo em grafo bipartido, por fases."""

    UNMATCHED = -1
    INFINITY = float('inf')

    def __init__(self, G, bipartition):
        self.G = G
        self.bipartition = bipartition
        self.V = G.V
        self.cardinality = 0

        # mate[v] = w  se a aresta v-w esta no emparelhamento
        # mate[v] = -1 se v nao esta emparelhado
        self.mate = [self.UNMATCHED] * self.V

        self.marked = None
        self.dist_to = None

        while self._has_augmenting_path():
            next_edge = [0] * self.V

            for s in range(self.V):
                if self._is_matched(s) or not self.bipartition.color(s):
                    continue

                path = [s]
                while path:
                    v = path[-1]

                    if next_edge[v] >= len(self.G.adj(v)):
                        path.pop()
                        continue

                    w = self.G.adj(v)[next_edge[v]]
                    next_edge[v] += 1

                    if not self._is_level_graph_edge(v, w):
                        continue

                    path.append(w)

                    if not self._is_matched(w):
                        while path:
                            x = path.pop()
                            y = path.pop()
                            self.mate[x] = y
                            self.mate[y] = x
                        self.cardinality += 1

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

    def _is_level_graph_edge(self, v, w):
        return self.dist_to[w] == self.dist_to[v] + 1 and self._is_residual_graph_edge(v, w)

    def _has_augmenting_path(self):
        """BFS a partir de TODOS os atiradores livres ao mesmo tempo.

        Responde duas coisas:
          1. ainda existe caminho aumentante?
          2. qual o nivel de cada vertice?
        Nao encontra nenhum caminho: isso e tarefa da DFS.
        """
        self.marked = [False] * self.V
        self.dist_to = [self.INFINITY] * self.V

        queue = deque()
        for v in range(self.V):
            if self.bipartition.color(v) and not self._is_matched(v):
                queue.append(v)
                self.marked[v] = True
                self.dist_to[v] = 0

        found = False
        while queue:
            v = queue.popleft()
            for w in self.G.adj(v):
                if self._is_residual_graph_edge(v, w):
                    if not self.marked[w]:
                        self.dist_to[w] = self.dist_to[v] + 1
                        self.marked[w] = True
                        if not self._is_matched(w):
                            found = True
                        if not found:
                            queue.append(w)
        return found

    def _is_matched(self, v):
        return self.mate[v] != self.UNMATCHED

    def size(self):
        return self.cardinality

    def is_perfect(self):
        return self.cardinality == self.bipartition.n


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])

    pairs = []
    for k in range(m):
        a = int(data[2 + 2 * k]) - 1       # entrada e 1..n, vetores sao 0..n-1
        b = int(data[3 + 2 * k]) - 1
        pairs.append((a, b))

    G = build_bipartite_graph(n, pairs)
    hk = HopcroftKarp(G, Bipartition(n))

    if not hk.is_perfect():
        sys.stdout.write("Impossible\n")
    else:
        output = "\n".join(str(hk.mate[i] - n + 1) for i in range(n))
        sys.stdout.write(output + "\n")


if __name__ == "__main__":
    main()
