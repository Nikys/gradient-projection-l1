from operator import itemgetter
from prioritydictionary import priorityDictionary
from math import inf

## @package YenKSP
# Computes K-Shortest Paths using Yen's Algorithm.
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph
# with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971
# and implores any shortest path algorithm to find the best path, then proceeds
# to find K-1 deviations of the best path.

## Computes K paths from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param start The source node of the graph.
# @param sink The sink node of the graph.
# @param K The amount of paths being computed.
#
# @retval [] Array of paths, where [0] is the shortest, [1] is the next
# shortest, and so on.
#


def ksp_yen(graph, node_start, node_end, max_k=2):
    distances, previous = dijkstra(graph, node_start)

    A = [{'cost': distances[node_end],
          'path': path(previous, node_start, node_end)}]
    B = []

    A[0]['distances'] = [distances[v] for v in A[0]['path']]

    if not A[0]['path']:
        return A

    for k in range(1, max_k):
        for i in range(0, len(A[-1]['path']) - 1):
            node_spur = A[-1]['path'][i]
            path_root = A[-1]['path'][:i + 1]
            spur_dist = A[-1]['distances'][i]

            edges_removed = []
            for path_k in A:
                curr_path = path_k['path']
                if len(curr_path) > i and path_root == curr_path[:i + 1]:
                    #length, cost = graph.remove_edge(curr_path[i], curr_path[i + 1])
                    disact_edge_result = graph.disactivate_edge(curr_path[i], curr_path[i + 1])
                    if not disact_edge_result:
                        continue
                    edges_removed.append([curr_path[i], curr_path[i + 1]])

            nodes_removed = []
            for node_ind in path_root:
                if node_ind == node_spur:
                    continue
                graph.disactivate_node(node_ind)
                nodes_removed.append(node_ind)
            path_spur = dijkstra(graph, node_spur, node_end)

            if path_spur['path']:
                path_total = path_root[:-1] + path_spur['path']
                distances = path_spur['distances']
                #dist_total = distances[node_spur] + path_spur['cost']
                dist_total = spur_dist + path_spur['cost']
                potential_dist = A[-1]['distances'][:i+1]
                dist_accum = potential_dist[-1]
                for p in path_spur['path'][1:]:
                    potential_dist.append(dist_accum + distances[p])
                potential_k = {'cost': dist_total, 'path': path_total, 'distances': potential_dist}
                #if len(set(path_total)) != len(path_total):
                #    potential_k = None

                if potential_k and potential_k not in B:
                    B.append(potential_k)

            for edge in edges_removed:
                graph.activate_edge(edge[0], edge[1])
                #graph.add_edge(edge[0], edge[1], edge[2], edge[3])
            for node_ind in nodes_removed:
                graph.activate_node(node_ind)
                #graph.add_edge(node_el.pair[0],node_el.pair[1],node_el.length,node_el.cost)

        if len(B):
            B = sorted(B, key=itemgetter('cost'))
            A.append(B[0])
            B.pop(0)
        else:
            break

    return A


## Computes the shortest path from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval {} Dictionary of path and cost or if the node_end is not specified,
# the distances and previous lists are returned.
#
def dijkstra(graph, node_start, node_end=None):
    distances = {}
    previous = {}
    Q = priorityDictionary()


    for v in graph:
        for u in v.neighbors:
            distances[u] = inf
            previous[u] = None
            Q[u] = inf

    distances[node_start] = 0
    Q[node_start] = 0

    for v in Q:
        if v == node_end: break
        v_node = graph.get_node(v)
        if not v_node.is_active():
            continue

        for u in v_node.neighbors:
            if not graph.get_node(u).is_active():
                continue
            edge = graph.get_edge(v,u)
            if not edge.is_active():
                continue
            cost_vu = distances[v] + edge.data.length

            if cost_vu < distances[u]:
                distances[u] = cost_vu
                Q[u] = cost_vu
                previous[u] = v

    if node_end:
        return {'cost': distances[node_end],
                'path': path(previous, node_start, node_end),
                'distances': distances}
    else:
        return (distances, previous)


## Finds a paths from a source to a sink using a supplied previous node list.
#
# @param previous A list of node predecessors.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval [] Array of nodes if a path is found, an empty list if no path is
# found from the source to sink.
#
def path(previous, node_start, node_end):
    route = []

    node_curr = node_end
    while True:
        route.append(node_curr)
        if previous[node_curr] == node_start:
            route.append(node_start)
            break
        elif previous[node_curr] is None:
            return []

        node_curr = previous[node_curr]

    route.reverse()
    return route

def min_paths(graph, pairs, max_k = 10):
    path_dict = dict()
    for p in pairs:
        if p not in path_dict:
            path_dict[p] = ksp_yen(graph=graph, node_start=p[0], node_end=p[1], max_k=max_k)
    return path_dict

## Finds mincost for path
#
# @param graph A digraph of class Graph.
# @param path A list of nodes indices.
#
# @retval Sum of mincosts
def mincost1(graph, path):
    sum_cost = 0
    for i in range(len(path)-1):
        sum_cost += graph.get_edge(path[i],path[i+1]).data.cost
    return sum_cost

## Finds mincost for list of paths
#
# @param graph A digraph of class Graph.
# @param paths A list of paths.
#
# @retval Min sum of mincosts
def mincost2(graph, paths, selfcost = 0.05):
    min_cost = -1
    for p in paths:
        if p[0] == p[-1]:
            return selfcost
        cost = mincost1(graph,p)
        if min_cost < 0 or cost < min_cost:
            min_cost = cost
    return min_cost

## Finds mincost for all lists of paths
#
# @param graph A digraph of class Graph.
# @param paths All lists of paths.
#
# @retval List of min sum of mincosts for every set of paths
def mincost3(graph,path_dict, selfcost = 0.05):
    cost_dict = dict()
    for pair,paths in path_dict.items():
        if pair not in cost_dict:
            cost_dict[pair] = mincost2(graph,[p['path'] for p in paths],selfcost)
    return cost_dict