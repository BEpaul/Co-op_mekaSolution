# graph = dict()

# graph['a'] = ['c']
# graph['b'] = ['c', 'e']
# graph['c'] = ['a', 'b', 'd', 'e']
# graph['d'] = ['c']
# graph['e'] = ['c', 'b']
# graph['f'] = []


# def dfs_recursive(graph, start, visited = []):
#     ## 데이터를 추가하는 명령어 / 재귀가 이루어짐 
#     visited.append(start)
 
#     for node in graph[start]:
#         if node not in visited:
#             dfs_recursive(graph, node, visited)
#     return visited



#w13 p30
# def dfs(graph, root, search):
#     visited = []
#     stack = [root, ]
#     while stack:
#         node = stack.pop()
#         if node not in visited:
#             visited.append(node)
#             if node == search:
#                 global found
#                 found = True
#                 break
#             stack.extend([x for x in graph[node] if x not in visited])
#     return visited;
    
# found = False
# graph = {'a' : ['c'], 'b' : ['c','e'], 'c' : ['a', 'b', 'd', 'e'], 'd' : ['c'], 'e' : ['c', 'b'], 'f' : []}
# print(dfs(graph, 'a', 'b'))
# if(found == True):
#     print("found")
# else:
#     print("not found")


# w13 p22

def dfs_recursive(graph, vertex, path):
    path += [vertex]
    for neighbor in graph[vertex]:
        if neighbor not in path:
            path = dfs_recursive(graph, neighbor, path)
    return path

adjacency_matrix = {'a': ['c'], 'b': ['c', 'e'], 'c': ['a','b','d','e'], 'd': ['c'], 'e': ['c','b'], 'f': []}

print(dfs_recursive(adjacency_matrix, 'a', []))

print('====================================')

# 깊이 구하기
