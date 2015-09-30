import time
import random
do_cs = True
do_erdos = True
do_graph = True
depth = 3

famous = {}
if do_cs:
    with open('famous_computer_scientists_wikipedia') as f:
        for line in f:
            line = line.split(':')
            lastname = line[0].split(' ')[-1].lower().strip()
            if lastname != '':
                if lastname in famous:
                    famous[lastname].extend(line)
                else:
                    famous[lastname] = line
    try:
        with open('famous_addendum') as f:
            for line in f:
                line = line.split(':')
                lastname = line[0].split(' ')[-1].lower().strip()
                if lastname != '':
                    if lastname in famous:
                        famous[lastname].extend(line)
                    else:
                        famous[lastname] = line
    except:
        pass

erdos = {}
if do_erdos:
    with open('ErdosA') as f:
        for n in range(22):
            f.readline()
        for line in f:
            lastname = line.split(',')[0].lower().strip()
            if line.isupper():
                erdos_number = 1
            else:
                erdos_number = 2
            if lastname in erdos:
                erdos[lastname].append(line.strip() + ' ::: ' + str(erdos_number))
            else:
                erdos[lastname] = [line.strip() + ' ::: ' + str(erdos_number)]

graph = {}
if do_graph:
    with open('author_graph_round_'+str(depth)) as f:
        for line in f:
            line = line.split(':')
            if len(line) < 2:
                continue
            node = line[0].strip()
            edges = line[1].split(',')
            graph[node] = []
            for edge in edges:
                if edge.strip() != '':
                    graph[node].append(edge.strip())


distance = {}
if do_graph:
    for n in range(0,depth+1):
        with open('round_' + str(n)) as f:
            authors = {}
            for line in f:
                line = line.split(';')
                name = line[0].strip()
                distance[name] = n
                if n == 0:
                    root = name

paths = []
def find_path(source, destination):
    path = []
    j = 0
    while destination != source:
        i = 0
        while i < (len(graph[source])) and i != -1:
            edge = graph[source][i]
            #print('in %s considering %s with distance %d' % (source, edge, distance[edge]))
            if distance.get(edge) is None or distance.get(source) is None:
                print('ugh we need a guaranteed bijection between the graph and the distance measure')
                i += 1
                continue
            if distance[edge] < distance[source]:
                path.append(source)
                #print('set %s to %s' % (source, edge))
                source = edge
                i = -1
            else:
                i += 1
        if i >= len(graph[source]):
            idx = random.randint(0,len(graph[source])-1)
            source = graph[source][idx]
            if graph.get(source) is None:
                j = 101
                print('ugh this graph needs to be guaranteed to be bidirectional')
        j += 1
        if j > 100:
            return ['???', ', '.join(path)]
    path.append(destination)
    paths.append(path)
    return path

erdos_count = 0
for n in range(1,depth+1):
    with open('round_' + str(n)) as f:
        authors = {}
        for line in f:
            line = line.split(';')
            name = line[0].strip()
            lastname = line[0].strip().split(' ')[-1].lower().strip()
            firstname = line[0].strip().split(' ')[0].lower().strip()
            if lastname != '':
                if do_cs and lastname in famous:
                    for i in range(0, len(famous[lastname]), 2):
                        if firstname in famous[lastname][i].lower():
                            print('%d: %s possibly found. From Wikipedia: %s' % (n, line[0].strip(), famous[lastname][i]))
                            if do_graph:
                                print('\t' + ', '.join(find_path(name,root)))
                            #time.sleep(2.5)
                if do_erdos and lastname in erdos and erdos_count < 10:
                    for i in range(len(erdos[lastname])):
                        if firstname in erdos[lastname][i].lower():
                            erdos_count += 1
                            print('%d: %s possibly found. %s erdos number' % (n, line[0].strip(), erdos[lastname][i]))
                            if do_graph:
                                print('\t' + ', '.join(find_path(name,root)))
                            #time.sleep(2.5)
                elif erdos_count == 10:
                    print('Too many Erdos numbers! Ignoring the rest...')
                    erdos_count += 1

if do_graph:
    out_nodes = {}
    for path in paths:
        if path[-2] in out_nodes:
            out_nodes[path[-2]] += 1
        else:
            out_nodes[path[-2]] = 1
print('out nodes:\n', out_nodes)
