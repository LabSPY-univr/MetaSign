positive_set = []


def checkMarkEdges(g, edge_visited):
    """
    Check if all edges of graph g have been marked
    :param g: graph
    :param edge_visited: property of bool value on each edge
    :return: True if all edges has been marked, False otherwise
    """
    for e in g.edges():
        if not edge_visited[e]:
            return False
    return True


def addPath(g, vertex_name, edge_visited, path):
    """
    Add path in path to the positive_set and mark each edge visited
    :param g: graph
    :param vertex_name: property with name for each vertex
    :param edge_visited: property marks on edges
    :param path: list of indices
    :return: None
    """
    if len(path) == 0:
        return
    string = ""
    for i in range(0, len(path)):
        if i == 0:
            continue
        edge_visited[g.edge(g.vertex(path[i-1]), g.vertex(path[i]))] = True  # edge from path[i-1] to path[i] is marked
    for i in path[0:len(path)-1]:  # last instruction excluded (ret)
        string += str(vertex_name[g.vertex(i)])
        string += ','
    #print(string[0:len(string)-1])  # last character excluded (,)
    positive_set.append(list(string[0:len(string)-1].split(',')))  # add the path as program to learn from


def printAllPathsUtil(g, vertex_name, u, d, k, edge_visited, path):
    """
    A recursive function to print all paths from 'u' to 'd' of length k.
    edge_visited[] keeps track of edges in current path.
    path[] stores actual vertices
    :param g: graph
    :param vertex_name: property with name for each vertex
    :param u: current source node
    :param d: node destination
    :param k: length of each path
    :param edge_visited: property marks on edges
    :param path: list of indices
    :return: True if all edges have been marked, False otherwise
    """
    path.append(u)

    # If current vertex is same as destination, then print current path[] only if is exactly of length k
    if u == d:
        if len(path) == k:
            addPath(g, vertex_name, edge_visited, path)
            if checkMarkEdges(g, edge_visited):
                return True
    elif len(path) < k:
        # If current vertex is not destination, recursive for all the vertices adjacent to this vertex
        for i in g.vertex(u).out_neighbours():
            if printAllPathsUtil(g, vertex_name, int(i), d, k, edge_visited, path):
                return True

    # Remove current vertex from path[]
    path.pop()
    return False


def printAllPaths(g, vertex_name, edge_visited, s, d, k):
    """
    Prints all paths from 's' to 'd' of length k in graph g
    :param g: graph
    :param vertex_name: property with name for each vertex
    :param edge_visited: property marks on edges
    :param s: node source
    :param d: node destination
    :param k: exact length of path
    :return: None
    """
    # Create a list to store paths
    path = []

    # Call the recursive helper function to print all paths
    return printAllPathsUtil(g, vertex_name, s, d, k, edge_visited, path)


def order1(e):
    """
    Order element e in terms of length of second position
    :param e: element
    :return: lenght
    """
    return len(e[1])


def order2(e):
    """
    Order element e in terms of alphabetical order of first position
    :param e: element
    :return: letters
    """
    return e[0]


def infer(positive_set):
    """
    Call inferRules() function at each pairs of variants and fill rules_inferred with all possible rules inferrable from positive_set
    :param positive_set: contains all variants to analyse
    :return: all rules inferred from positive_set
    """
    rules_inferred = []
    for var1 in positive_set:
        for var2 in positive_set:
            if var1 == var2:
                continue
            if len(var1) >= len(var2):
                continue
            rules = inferRules(var1, var2)
            if len(rules) > 0:
                for r in rules:
                    if r not in rules_inferred:
                        rules_inferred.append(r)
    rules_inferred = sorted(rules_inferred, key=order1)
    return rules_inferred


def inferRules(var1, var2):
    """
    Return all rules R such that var1 --R-> var2 with an application of rule R
    Return an empty list in case rules  of the form 1->r are not inferable
    :param var1: first variant (smaller)
    :param var2: second variant (bigger)
    :return: rules inferred from var1 and var2
    """
    rules = []

    # left simplify first then right
    str1 = var1.copy()
    str2 = var2.copy()
    i = 0
    while True:
        if len(str1) == 1:
            if len(str2) == 2: rules.append([str1[0], str2.copy()])
            break
        if str1[i] == str2[i]:
            str1.pop(i)
            str2.pop(i)
        else:
            if i == 0:
                i = -1
            else:
                if len(str1) == 1:
                    if len(str2) == 2: rules.append([str1[0], str2.copy()])
                break

    # right simplify first then left
    str1 = var1.copy()
    str2 = var2.copy()
    i = -1
    while True:
        if len(str1) == 1:
            if [str1[0], str2] not in rules:
                if len(str2) == 2: rules.append([str1[0], str2.copy()])
            break
        if str1[i] == str2[i]:
            str1.pop(i)
            str2.pop(i)
        else:
            if i == -1:
                i = 0
            else:
                if len(str1) == 1:
                    if [str1[0], str2] not in rules:
                        if len(str2) == 2: rules.append([str1[0], str2.copy()])
                break

    # left and right concurrently
    str1 = var1.copy()
    str2 = var2.copy()
    i = 0
    while True:
        if len(str1) == 1:
            if [str1[0], str2] not in rules:
                if len(str2) == 2: rules.append([str1[0], str2.copy()])
            break
        if str1[i] == str2[i]:
            str1.pop(i)
            str2.pop(i)
            if i == 0:
                i = -1
            else:
                i = 0
        else:
            if len(str1) == 1:
                if [str1[0], str2] not in rules:
                    if len(str2) == 2: rules.append([str1[0], str2.copy()])
            break

    return rules


def printRules(rules_inferred):
    """
    Print all rules in rules_inferred
    :param rules_inferred: list of rules
    :return: None
    """
    for r in sorted(rules_inferred, key=order2):
        print(r[0], end='')
        print(' -> ', end='')
        print(r[1])


def contains(small, big):
    """
    Return (-1, -1) if small is not contained in big, an interval of first occur otherwise
    :param small: list of instructions smaller than big
    :param big: list of instructions bigger than small
    :return: the interval (i, j) if it is contained, (-1, -1) otherwise
    """
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return -1, -1


def substitute(op, rlist, bound):
    """
    Substitute interval (bound[0], bound[1]-1) with operand op (modify rlist!) in rlist
    :param op: operand to sobstitute
    :param rlist: list of instructions
    :param bound: interval to sobstitute with op
    :return: None
    """
    rlist[bound[0]:bound[1]] = [op]


def simplify(base, rule_c):
    """
    Return True if rule_c (no modify) is reducible to one rule in base, False otherwise
    :param base: list of base rules to apply
    :param rule_c: rule to test
    :return: True if rule_c can be removed (since is subsumed by another rule), False otherwise
    """
    new_b = []
    for i in range(0, len(base)):
        rule = rule_c.copy()
        if i > 0:
            new_b = base[i:]+base[0:i]
        for r in new_b:
            i, j = contains(r[1], rule[1])
            while i != -1 and j != -1:  # then r is applicable in rule as compression
                substitute(r[0], rule[1], (i, j))
                if rule in base:
                    return True
                if len(rule[1]) == 2:
                    return False
                i, j = contains(r[1], rule[1])
    return False


def start_simplify(rules):
    """
    Remove from rules all the rules that are reachable from other smaller rules
    :param rules: list of rules to simplify
    :return: None
    """
    to_remove = []
    base = []
    # setting base rules (those with left hand size 2)
    i = 0
    for i in range(0, len(rules)):
        if len(rules[i][1]) == 2:
            base.append(rules[i])
        else:
            break
    # try to subsume other rules and, if not, adding those to base rules
    for r in rules[i:]:
        if simplify(base, r.copy()):
            to_remove.append(r)
        else:
            base.append(r)
    # removing all rules subsumed
    for t in to_remove:
        rules.remove(t)
