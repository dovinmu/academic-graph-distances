
fname1 = 'knuth/author_graph_round_3'
fname2 = 'hofstadter/author_graph_round_3'
name1 = 'Donald E. Knuth'
name2 = 'Douglas Hofstadter'

skipped = 0
graph = {}
with open(fname1) as f:
    for line in f:
        line = line.split(':')
        if len(line) < 2:
            #print('something is missing... ' + ': '.join(line))   
            skipped += 1
            continue
        node = line[0].strip()
        edges = line[1].split(',')
        graph[node] = set()
        for edge in edges:
            if edge.strip() != '':
                graph[node].add(edge.strip())

with open(fname2) as f:
    for line in f:
        line = line.split(':')
        if len(line) < 2:
            #print('something is missing... ' + ': '.join(line))
            skipped += 1
            continue
        node = line[0].strip()
        edges = line[1].split(',')
        if node not in graph:
            graph[node] = set()
        for edge in edges:
            if edge.strip() != '':
                graph[node].add(edge.strip())
nodes = len(graph)
edges = 0
for key in graph.keys():
    edges += len(graph[key])

print('graph processed. %.2fk nodes, %.2fk edges, and %d skipped entries' % (nodes/1000, edges/1000, skipped))


def dijkstra(source):    
    distance = {}
    prev = {source:None}
    unvisited = set()
    leaves = [set()] #a priority queue
    for node in graph.keys():
        distance[node] = float('inf')
        unvisited.add(node)
    distance[source] = 0
    while len(unvisited) > 0:
        for node in graph[source]:
            if node in unvisited:
                new_dist = distance[source] + 1
                if new_dist < distance[node]:
                    if math.isfinite(distance[node]):
                        leaves[distance[node]].remove(node)
                    while len(leaves) < new_dist+1:
                        leaves.append(set())
                    leaves[new_dist].add(node)
                    distance[node] = new_dist
                    prev[node] = source
        unvisited.remove(source)

        i = 0
        while len(leaves[i]) == 0:
            i += 1
            if i == len(leaves):
                break
        if i == len(leaves):
            break
        source = leaves[i].pop()
        if source not in unvisited:
            print('we have a problem...')
            return
        print('%.2fk nodes left' % (len(unvisited)/1000),end='\r')
    print('                                    ')
    return prev

paths = dijkstra(name1)

def shortest_path(dest):
    path = []
    pathfinder = dest
    if paths.get(dest):
        while pathfinder != None:
            path.append(pathfinder)
            pathfinder = paths[pathfinder]
        path.append(distance[dest])
    return path

shortest_path(name2)
