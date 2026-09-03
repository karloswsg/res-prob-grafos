"""
beecrowd 1100 - Movimentos do Cavalo (Knight Moves)
Problema F - Grupo A

Adaptado de algs4-py: Graph e BreadthFirstPaths.
Adaptacoes:
  1. construcao implicita do grafo (regra do cavalo, sem leitura de arquivo)
  2. vetor dist_to acrescentado ao BreadthFirstPaths
  3. leitura da entrada no formato do problema, ate EOF
"""
import sys
from collections import deque

class Graph:
    """Lista de adjacencia. Adaptado de algs4.graph (Bag trocado por list)."""

    def __init__(self, V):
        self.V = V
        self.E = 0
        self.adj = [[] for _ in range(V)]

    def add_edge(self, v, w):
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1

    def degree(self, v):
        return len(self.adj[v])

N = 8
SALTOS = [(1, 2), (2, 1), (2, -1), (1, -2),
          (-1, -2), (-2, -1), (-2, 1), (-1, 2)]

def id_vertice(coluna, linha):
    """Converte (coluna, linha) em indice 0..63."""
    return linha * N + coluna

def constroi_tabuleiro():
    """Gera o grafo do cavalo 8x8 pela regra de movimento."""
    G = Graph(N * N)
    for linha in range(N):
        for coluna in range(N):
            v = id_vertice(coluna, linha)
            for dc, dl in SALTOS:
                c, l = coluna + dc, linha + dl
                if 0 <= c < N and 0 <= l < N:
                    w = id_vertice(c, l)
                    if v < w:
                        G.add_edge(v, w)
    return G

G = constroi_tabuleiro()

class BreadthFirstPaths:
    """Adaptado de algs4.breadth_first_paths, com dist_to acrescentado."""

    def __init__(self, G, s):
        self.marked = [False] * G.V
        self.edge_to = [-1] * G.V
        self.dist_to = [-1] * G.V
        self.s = s
        self.bfs(G, s)

    def bfs(self, G, s):
        self.marked[s] = True
        self.dist_to[s] = 0
        fila = deque([s])
        while fila:
            v = fila.popleft()
            for w in G.adj[v]:
                if not self.marked[w]:
                    self.marked[w] = True
                    self.edge_to[w] = v
                    self.dist_to[w] = self.dist_to[v] + 1
                    fila.append(w)

    def has_path_to(self, v):
        return self.marked[v]

def le_casa(texto):
    """Converte 'e2' em indice 0..63."""
    coluna = ord(texto[0]) - ord('a')
    linha = int(texto[1]) - 1
    return id_vertice(coluna, linha)

def main():
    G = constroi_tabuleiro()
    for linha in sys.stdin:
        partes = linha.split()
        if len(partes) < 2:
            continue
        origem, destino = partes[0], partes[1]
        bfs = BreadthFirstPaths(G, le_casa(origem))
        n = bfs.dist_to[le_casa(destino)]
        print("To get from %s to %s takes %d knight moves." % (origem, destino, n))

if __name__ == '__main__':
    main()
