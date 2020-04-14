import random

num_vertices = 100

file = 'inputs/' + str(num_vertices) + '.in'
graph = [[] for _ in range(num_vertices)]
vertices = list(range(num_vertices))
random.shuffle(vertices)
# generate tree
u = 0
for v in vertices:
    if v != 0:
        graph[u].append(v)
        u = v

# add extra edges
complete_graph = num_vertices * (num_vertices + 1) / 2
num_edges = int((complete_graph - num_vertices + 1) * random.random())

while num_edges > 0:
    v = int(random.uniform(0, num_vertices))
    u = int(random.uniform(0, num_vertices))
    if v != u and v not in graph[u] and u not in graph[v]:
        graph[u].append(v)
        num_edges -= 1

with open(file, 'w') as f:
    f.write(str(num_vertices) + '\n')

    for u in range(len(graph)):
        for v in graph[u]:
            w = round(random.uniform(0.001, 99.999), 3)
            f.write('{0} {1} {2}\n'.format(u, v, w))
