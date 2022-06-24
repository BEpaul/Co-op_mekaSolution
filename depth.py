from traceback import print_tb


def dfs_r(graph, current_node, visit_path):
    visit_path.append(current_node)
    for neighbor in graph[current_node]:
        if neighbor not in visit_path:
            visit_path = dfs_r(graph, neighbor, visit_path)
    return visit_path

adj_matrix = {1: [2,5,4], 2: [4,5,7], 3: [5,2], 4: [7], 5: [6], 6: [7,8], 7: [], 8:[7,4]}
result = []
dfs_r(adj_matrix, 1, result)
print(result)