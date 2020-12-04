def printPath(g, vertex_name, path):
    if len(path) == 0:
        return
    string = ""
    for i in path[0:len(path)-1]:
        string += str(vertex_name[g.vertex(i)])
        string += ','
    print(string[0:len(string)-1])


'''A recursive function to print all paths from 'u' to 'd'.
    visited[] keeps track of vertices in current path.
    path[] stores actual vertices and path_index is current
    index in path[]'''
def printAllPathsUtil(g, vertex_name, u, d, visited, path):
    # Mark the current node as visited and store in path
    visited[g.vertex(u)] = True
    path.append(u)

    # If current vertex is same as destination, then print current path[]
    if u == d:
        printPath(g, vertex_name, path)
    else:
        # If current vertex is not destination recursive for all the vertices adjacent to this vertex
        for i in g.vertex(u).out_neighbours():
            if not visited[i]:
                printAllPathsUtil(g, vertex_name, int(i), d, visited, path)

    # Remove current vertex from path[] and mark it as unvisited
    path.pop()
    visited[u] = False


# Prints all paths from 's' to 'd' in graph g
def printAllPaths(g, vertex_name, s, d):
    # Mark all the vertices as not visited
    visited = g.new_vertex_property("bool")

    # Create a list to store paths
    path = []

    # Call the recursive helper function to print all paths
    printAllPathsUtil(g, vertex_name, s, d, visited, path)

roots = getRoots(graph_wdn, vertex_shape_wdn)
for v in roots:
    printAllPaths(graph_wdn, vertex_name_wdn, int(v), int(getRet(graph_wdn)))
