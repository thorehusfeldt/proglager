# Edmonds-Karp with multiedges and capacity scaling

from collections import defaultdict
from collections import deque

n, m, s, t, = map(int, raw_input().split())

N = defaultdict(list) # neighbourhood lists, N[u] = [(w_1, cap_1), (w_2, cap_2), ...] 
R = [dict() for _ in range(n)] # R[u][v] = residual cap in G_f from u to v in G_f
C = [dict() for _ in range(n)] # C[u][v] = total cap in G from u to v in G

maxcap = 0
for _ in range(m):
    u, v, cap = map(int, raw_input().split())
    N[u].append((v,cap))
    R[u][v] = cap if v not in R[u] else R[u][v] + cap   # edge already there? increase cap
    R[v][u] = 0 if u not in R[v] else R[v][u]           # same on res edge
    C[u][v] = R[u][v]                                   # remember total cap of instance
    maxcap = max(maxcap , C[u][v])                      # need this for cap scaling 

cutoff = maxcap // 2

def BFS(s, t, parent):
    Q = deque([s])
    M = [False] * n
    M[s] = True
    while Q:
        u = Q.popleft()
        for v, res_cap  in R[u].items():
            if (M[v] == False) and (res_cap > cutoff):  # or .. > 0 if cap scaling not necc.
                Q.append(v)
                M[v] = True
                parent[v] = u
    return M[t]                       # the cut would be in M, but here we don't need it

pred = [None] * n
flow = 0
while (True):
    while (BFS(s,t,pred)):
        f_p = float('inf')
        v = t
        while (v != s):
            u = pred[v]
            f_p = min(f_p, R[u][v])
            v = u
        flow += f_p
        v = t
        while (v != s):
            u = pred[v]
            R[u][v] -= f_p
            R[v][u] += f_p
            v = u
    if cutoff == 0: break
    cutoff = cutoff // 2

flow_edges = 0
string = ""
for u in range(n):
    for v, cap in N[u]:
        if R[u][v] < C[u][v]:
            flow_edges += 1
            f_e = min(C[u][v] - R[u][v], cap)
            string += "{} {} {}\n".format( u, v, f_e)
            R[u][v] -= f_e
            C[u][v] -= f_e

print n, flow, flow_edges
print string




