"""
Kattis Paintball - Problema I - Grupo A
Hopcroft-Karp adaptado de algs4/HopcroftKarp.java
"""

import sys
from collections import deque

INF = float('inf')

class HopcroftKarp:
    
    UNMATCHED = -1

    def __init__(self, n, adj):
        self.n = n
        self.adj = adj
        self.mate_shooter = [self.UNMATCHED] * n    # 
        self.mate_target = [self.UNMATCHED] * n     # 
        self.dist = [INF] * n                       # 
        self.cardinality = 0
        while self._has_augmenting_path():          # 
            for v in range(n):
                if self.mate_shooter[v] == self.UNMATCHED and self._dfs(v):
                    self.cardinality += 1

    def is_perfect(self):
        return self.cardinality == self.n

    def _has_augmenting_path(self):
        """BFS de fase: calcula os niveis a partir de todos os atiradores livres."""
        fila = deque()
        for v in range(self.n):
            if self.mate_shooter[v] == self.UNMATCHED:
                self.dist[v] = 0
                fila.append(v)
            else:
                self.dist[v] = INF
        achou = False
        while fila:                         # 
            v = fila.popleft()
            dv = self.dist[v]
            for w in self.adj[v]:           # w e ALVO
                u = self.mate_target[w]     # u e ATIRADOR que ocupa esse alvo
                if u == self.UNMATCHED:     # chegou ao fim do caminho aumentante -> nao tem mais atirador pra enfileirar
                    achou = True
                elif self.dist[u] == INF:   # marcacao de visita
                    self.dist[u] = dv + 1
                    fila.append(u)
        return achou

    def _dfs(self, v):
        """Colhe um caminho aumentante minimo, so por arestas que sobem um nivel."""
        for w in self.adj[v]:
            u = self.mate_target[w]
            if u == self.UNMATCHED or (self.dist[u] == self.dist[v] + 1 and self._dfs(u)):
                # 
                self.mate_shooter[v] = w
                self.mate_target[w] = v
                return True
        self.dist[v] = INF
        return False
        # sem isso o algoritmo deixa de ser O(E raiz de V)


def main():
    sys.setrecursionlimit(300000)
    dados = sys.stdin.buffer.read().split()
    n = int(dados[0])
    m = int(dados[1])

    adj = [[] for _ in range(n)]
    for k in range(m):
        a = int(dados[2 + 2 * k]) - 1
        b = int(dados[3 + 2 * k]) - 1
        adj[a].append(b)
        adj[b].append(a)

    hk = HopcroftKarp(n, adj)

    if not hk.is_perfect():
        sys.stdout.write("Impossible\n")
    else:
        saida = "\n".join(str(hk.mate_shooter[v] + 1) for v in range(n))
        sys.stdout.write(saida + "\n")


if __name__ == "__main__":
    main()
