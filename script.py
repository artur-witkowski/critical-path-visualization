import json
from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt


def dfs_cycle_detect(graph, node, visited, rec_stack, stack):
    visited[node] = True
    rec_stack[node] = True

    for adjacent in graph[node]:
        if visited[adjacent] == False:
            if dfs_cycle_detect(graph, adjacent, visited, rec_stack, stack):
                return True
        elif rec_stack[adjacent] == True:
            return True

    stack.append(node)
    rec_stack[node] = False
    return False


def topological_sort(graph, nodes):
    visited = defaultdict(bool)
    rec_stack = defaultdict(bool)
    stack = []
    for node in nodes:
        if visited[node] == False:
            if dfs_cycle_detect(graph, node, visited, rec_stack, stack) == True:
                return True, []
    stack.reverse()
    return False, stack


def longest_path(graph, nodes, task_times):
    dist = {node: -float("inf") for node in nodes}
    in_degree = {node: 0 for node in nodes}
    previous = {node: None for node in nodes}

    for node in nodes:
        for adjacent in graph[node]:
            in_degree[adjacent] += 1

    start_nodes = [node for node in in_degree if in_degree[node] == 0]

    for node in start_nodes:
        dist[node] = task_times[node]

    for node in nodes:
        for adjacent in graph[node]:
            if dist[adjacent] < dist[node] + task_times[adjacent]:
                dist[adjacent] = dist[node] + task_times[adjacent]
                previous[adjacent] = node

    max_dist = max(dist.values())
    end_node = [node for node, distance in dist.items() if distance == max_dist][0]
    path = build_path(previous, end_node)

    return path, dist, max_dist


def build_path(previous, end_node):
    path = []
    while end_node is not None:
        path.append(end_node)
        end_node = previous[end_node]
    return path[::-1]


def schedule_tasks(dist):
    schedule = []
    for node, time in sorted(dist.items(), key=lambda item: item[0]):
        schedule.append(f"{node} ({time - task_times[node]}-{time})")
    return schedule


def draw_graph(graph, critical_path):
    G = nx.DiGraph()

    for node, adjacents in graph.items():
        for adjacent in adjacents:
            G.add_edge(node, adjacent)

    color_map = []
    for node in G:
        if node in critical_path:
            color_map.append("red")
        else:
            color_map.append("green")

    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=color_map, with_labels=True)
    plt.show()


with open("input.json", "r") as file:
    data = file.read()

data = json.loads(data)
graph = defaultdict(list)
task_times = data["nodes"]

for edge in data["edges"]:
    graph[edge[0]].append(edge[1])

cycle, sorted_nodes = topological_sort(graph, list(task_times.keys()))
if cycle:
    print("Błąd: Graf zawiera cykl, nie można wyznaczyć ścieżki krytycznej.")
else:
    critical_path, dist, max_dist = longest_path(graph, sorted_nodes, task_times)
    print("Ścieżka krytyczna:", " -> ".join(critical_path))
    print("Uszeregowanie zadań:", ", ".join(schedule_tasks(dist)))
    print("Łączny czas wykonania:", max_dist, "dni")

draw_graph(graph, critical_path)
