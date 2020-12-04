import random
from graph_tool.all import *
from collections import deque

program = []
abstract_program = []
registers = ["eax", "ebx", "ecx", "edx", "esp", "ebp", "esi", "edi"]
operation = ["pop", "push", "nop", "mov", "cmp", "add", "sub", "and", "xor", "test", "lea"]
cond_branch = ["je", "jne", "jl", "jle", "jg", "jge"]
branch = ["jmp", "call"]
stack = []
dict_graph = {}
graph_wdn = Graph()
abs_ins_wdn = graph_wdn.new_vertex_property("object")
lang_wdn = graph_wdn.new_vertex_property("object")
mark_wdn = graph_wdn.new_vertex_property("bool")
vertex_name_wdn = graph_wdn.new_vertex_property("string")
vertex_shape_wdn = graph_wdn.new_vertex_property("string")
to_merge = []
nstats = [0, 0, 0]
nrules = [-1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def stats():
    """
    Print statistics on rules applied
    :return: None
    """
    print("nexp = ", nstats[0])
    print("ncomp = ", nstats[1])
    print("changes = ", nstats[2])
    print("nrules = ")
    print(nrules)


def printGraph(g, vertex_name, vertex_sh, output=False):
    """
    Print a plot for graph g
    :param g: graph to plot
    :param vertex_name: name to verteces
    :param vertex_sh: shape to verteces
    :param output: if True save it to file
    :return: None
    """
    graph_draw(g, vertex_text=vertex_name, vertex_shape=vertex_sh, vertex_font_size=10, vertex_size=5, edge_pen_width=2)
    if output:
        graph_draw(g, vertex_text=vertex_name, vertex_shape=vertex_sh, vertex_font_size=10, vertex_size=5, edge_pen_width=2, output="test/wdn_result.png")


def optype(op):
    """
    Return which kind of instruction is op
    :param op: the instruction
    :return: 0 if an operation, 1 if conditional branch, 2 if a branch, 3 if ret instruction
    """
    if op in operation:
        return 0
    elif op in cond_branch:
        return 1
    elif op in branch:
        return 2
    else:
        return 3  # ret


def itype(op):
    """
    Return which kind of operand is op
    :param op: the operand
    :return: 0 if register, 1 if memory adress, 2 if immediate
    """
    if op in registers:  # tipo registro
        return 0
    elif '[' in op:      # tipo memoria
        return 1
    else:                # tipo valore immediato
        return 2


def randomReg():
    """
    Return a random register
    :return: a random register
    """
    n = random.randint(0, len(registers)-1)
    return registers[n]


def randomMem():
    """
    Return a random number
    :return: a random number
    """
    n = random.randint(10000, 100000)
    return '[' + str(n) + ']'


def fixAdr(exp, ppoint):
    """
    Fix all adresses in program
    :param exp: last rule applied
    :param ppoint: on which program point
    :return: None
    """
    for adr in range(0, len(program)):
        if (optype(program[adr][0]) == 1) or (optype(program[adr][0]) == 2):
            if int(program[adr][1]) > ppoint:
                if exp == 1:
                    new_adr = int(program[adr][1]) + 1
                    program[adr][1] = str(new_adr)
                else:
                    new_adr = int(program[adr][1]) - 1
                    program[adr][1] = str(new_adr)


def genGraph(g, m):
    """
    Generate the CFG of program as graph in g with property m
    :param g: the graph to construct the CFG
    :param m: boolean property of g
    :return: None
    """
    dict_graph.clear()
    stack.clear()
    last_address = -1
    last_type = -1
    current_adress = 0
    current_type = optype(program[current_adress][0])

    while current_adress != len(program):
        dict_graph[current_adress] = []  # add_vertex(G, ins)

        if (last_type == 0) or (last_type == 1):  # operation or cond_branch
            dict_graph[last_address].append(current_adress)  # add_edge(G, last_address, ins.address)
        if (current_type == 1) or (current_type == 2):  # cond_branch or branch
            dict_graph[current_adress].append(int(program[current_adress][1]))  # add_edge(G, ins.address, ins.target_address)

        last_address = current_adress
        last_type = current_type
        if program[current_adress][0] == "call":
            stack.append(current_adress+1)
            current_adress = int(program[current_adress][1])
        elif program[current_adress][0] == "ret":
            if len(stack) == 0:
                break
            adr = stack.pop()
            dict_graph[current_adress].append(adr)
            current_adress = adr
        else:
            current_adress += 1
        current_type = optype(program[current_adress][0])

    # converting the graph in the dictionary into a real graph structure
    g.add_vertex(len(dict_graph.keys()))
    for v in dict_graph.keys():
        m[v] = False
        for succ in dict_graph[v]:
            g.add_edge(v, succ)


def find_paths(node, n, path=[]):
    """
    Returns all nodes in a path of lenght n
    :param node: pointer to a node
    :param n: lenght
    :param path: list
    :return: the path
    """
    path += [node]  # qui node è un puntatore e non uno scalare
    if (n == 0) or (node.out_degree() == 0 and n != 0):
        return [path]
    paths = []
    for q in node.out_neighbours():
        if q not in path:
            newpaths = find_paths(q, n-1, path)
            for newpath in newpaths:
                paths.append(newpath)
    return paths


def genLang(n, g, lang):
    """
    Generate the language of lenght n for each node in graph g
    :param n: lenght of the language
    :param g: the graph
    :param lang: property to save the language
    :return:
    """
    if n == 0:
        return
    for v in g.vertices():
        lang[v] = find_paths(v, n-1, [])


def printLang(g, lang):
    """
    Print the language of each node in g (index value)
    :param g: graph
    :param lang: property of g in which language is saved
    :return: None
    """
    for v in g.vertices():
        print(int(v), end=": ")
        ll = []
        for seq in lang[v]:
            l = []
            for n in seq:
                l.append(int(n))
            ll. append(l)
        print(ll, end=", ")
    print()


def genAbstraction(instruction):
    """
    Abstraction on a single instruction (in this abstraction, only the operations are considered)
    :param instruction: instruction
    :return: abstracted instruction
    """
    if len(instruction) == 3:
        return [instruction[0], "T", "T"]
    elif len(instruction) == 2:
        return [instruction[0], "T"]
    else:
        return [instruction[0]]


def setAbstraction(g, abs_ins, vertex_name):
    """
    Generate an abstraction of program in the graph g in property abs_ins
    :param g: graph
    :param abs_ins: property of g to save the abstracted instruction
    :param vertex_name: property to save the name of each vertex
    :return: None
    """
    i = 0
    for ins in program:
        abs_ins[g.vertex(i)] = genAbstraction(ins)
        vertex_name[g.vertex(i)] = str(abs_ins[g.vertex(i)][0])  # names in nodes on the plot
        i += 1


def genAbstractProgram():
    """
    Generate an abstraction of current program in abstract_program for the positive_set
    :return: None
    """
    abstract_program.clear()
    for ins in program:
        abstract_program.append(ins[0])
    abstract_program.pop()  # remove 'ret' instruction


def printAbstraction(g, abs_ins):
    """
    Print the abstract instruction of each vertex in g
    :param g: the graph
    :param abs_ins: property of g containing the abstract instructions of each vertex
    :return: None
    """
    for v in g.vertices():
        print(abs_ins[v], end=", ")
    print()


def clousure(abs_ins, seq):
    """
    Generate the transitive closure of each node in seq respect to the abstract instructions
    :param abs_ins: property containing the abstract instructions of each vertex
    :param seq: list of nodes to apply this function
    :return: the transitive clousure
    """
    setseq = set()
    listtup = []
    i = 0
    for v in seq:  # v is a pointer to a node in the graph
        if len(abs_ins[v]) == 3:
            listtup.append((abs_ins[v][0], abs_ins[v][1], abs_ins[v][2]))
        elif len(abs_ins[v]) == 2:
            listtup.append((abs_ins[v][0], abs_ins[v][1]))
        else:
            listtup.append(abs_ins[v][0])
        if i == 0:
            setseq.add(listtup[0])
            i += 1
        else:
            setseq.add(tuple(listtup))
    return setseq


def checkLang(abs_ins1, abs_ins2, lang1, lang2):
    """
    Check if lang1 and lang2 (with his respective abstract instr) recognize the same language
    :param abs_ins1: property containing the abstract instructions of each vertex for lang1
    :param abs_ins2: property containing the abstract instructions of each vertex for lang2
    :param lang1: lang to compare
    :param lang2: lang to compare
    :return: True if they are the same language, False otherwise
    """
    setlang1 = set()
    setlang2 = set()

    for seq in lang1:
        setlang1 |= clousure(abs_ins1, seq)  # set union
    for seq in lang2:
        setlang2 |= clousure(abs_ins2, seq)  # set union

    if len(setlang1 - setlang2) == 0 & len(setlang2 - setlang1) == 0:
        return True
    return False


def markNodes_old(g1, g2, m1, m2, lang1, lang2, abs_ins1, abs_ins2, next=1000):  # mark PAIRS of nodes from g1 (widening) and g2 (variant) with the same language
    to_merge.clear()
    offset = g1.num_vertices()
    for v in g2.vertices():
        count = next  # visito al massimo next nodi a partire dal nodo di g1
        for d in g1.vertices():
            if m1[d]:  # se True vuol dire che è già marcato come equivalente ad un altro nodo
                continue
            if count == 0:
                break
            count -= 1
            if checkLang(abs_ins2, abs_ins1, lang2[v], lang1[d]):
                to_merge.append((int(v)+offset, int(d)))  # to_merge contiene solo gli indici (di cui quelli della variante spostati dell'offset per quando saranno uniti nel grafo del wdn) dei nodi di cui fare il merge
                m2[v] = True
                m1[d] = True
                break


def markNodes_new(g, m, abs_ins, lang):
    """
    Mark ALL nodes in g with the same language
    :param g: the graph
    :param m: boolean property of g (all 0)
    :param abs_ins: abstract instructions of g
    :param lang: language of each vertex in g
    :return: None
    """
    to_merge.clear()
    to_merge.append([])
    for v in g.vertices():
        for d in g.vertices():
            if int(v) == int(d):
                continue
            if m[d]:  # se True vuol dire che è già marcato come equivalente ad un altro nodo
                continue
            if checkLang(abs_ins, abs_ins, lang[v], lang[d]):
                if not m[v]:
                    to_merge[-1].append(int(v))
                    m[v] = True
                to_merge[-1].append(int(d))  # to_merge contains indexes only
                m[d] = True
        if len(to_merge[-1]) > 0:
            to_merge.append([])
    to_merge.pop()


def getRoots(g, vertex_shape):
    """
    Return a list of pointers to all roots in graph g (those nodes with double circle)
    :param g: graph
    :param vertex_shape: property shape for each node
    :return: list of pointers to roots
    """
    roots = []
    for v in g.vertices():
        if vertex_shape[v] == "double_circle":
            roots.append(v)
    return roots


def getRet(g):
    """
    Return the node containing the last instruction (ret)
    :param g: graph
    :return: node pointer to 'ret' instruction
    """
    for v in g.vertices():
        if v.out_degree() == 0:
            return v


def markNodes_roots(g1, g2, m1, m2, lang1, lang2, abs_ins1, abs_ins2, vertex_shape1, vertex_shape2, next=1000):  # mark PAIRS of nodes from g1 (widening) and g2 (variant) with the same language starting from a root and return True if all nodes in g2 are marked as True (fix point reached)
    to_merge.clear()
    offset = g1.num_vertices()
    roots_g1 = getRoots(g1, vertex_shape1)  # il grafo g1 lo visito sempre a partire dalle sue radici
    queue_g1 = deque()
    count_mark = 0  # conta quanti nodi di g2 vengono markati da unire
    for v in g2.vertices():  # parte sicuramente dal nodo root in quanto ha id 0
        count = next  # visito al massimo next nodi a partire dal nodo di g1
        queue_g1.extend(roots_g1)
        while len(queue_g1) != 0 and count != 0:
            d = queue_g1.popleft()
            if m1[d]:  # se True vuol dire che è già marcato come equivalente ad un altro nodo
                queue_g1.extend(d.out_neighbours())
                continue
            if checkLang(abs_ins2, abs_ins1, lang2[v], lang1[d]):
                to_merge.append((int(v)+offset, int(d)))  # to_merge contiene solo gli indici (di cui quelli della variante spostati dell'offset per quando saranno uniti nel grafo del wdn) dei nodi di cui fare il merge
                m2[v] = True
                count_mark += 1
                m1[d] = True
                break
            count -= 1
            queue_g1.extend(d.out_neighbours())
    if count_mark == g2.num_vertices():
        return True
    else:
        return False


def printMark():
    print("to_merge = variant , wdn")
    for v,t in to_merge:
        print(v, end=" , ")
        print(t)


def printMark_new():
    print("to_merge")
    for n in to_merge:
        for v in n:
            print(v, end=", ")
        print()


def mergeNodes(g, nodes, abs_ins, vertex_name, vertex_shape):
    """
    Merge all nodes in the nodes list. nodes is an index list (not pointers to nodes)
    :param g: the graph
    :param nodes: list of nodes in g to merge
    :param abs_ins: their abstract instructions
    :param vertex_name: property
    :param vertex_shape: property
    :return: None
    """
    to_remove = []  # old edges to be removed
    to_add = []  # new edges to add
    new_node = g.add_vertex()  # Add the 'merged' node
    abs_ins[new_node] = abs_ins[g.vertex(nodes[0])]
    vertex_name[new_node] = vertex_name[g.vertex(nodes[0])]
    vertex_shape[new_node] = "circle"
    for node in nodes:  # if one node in nodes is a root then also new_node will be a root
        if vertex_shape[g.vertex(node)] == "double_circle":
            vertex_shape[new_node] = "double_circle"
            break
    for e in g.edges():
        # For all edges related to one of the nodes to merge,
        # make an edge going to or coming from the `new generated one`
        n1, n2 = e
        if (int(n1) in nodes) and (int(n2) in nodes):
            if (new_node, new_node) not in to_add:  # add only if it does not exist
                to_add.append((new_node, new_node))
            to_remove.append(e)
        elif int(n1) in nodes:
            if (new_node, n2) not in to_add:
                to_add.append((new_node, n2))
            to_remove.append(e)
        elif int(n2) in nodes:
            if (n1, new_node) not in to_add:
                to_add.append((n1, new_node))
            to_remove.append(e)

    for n1, n2 in to_add:  # add new edges
        g.add_edge(n1, n2)
    for e in to_remove:  # remove the old edges
        g.remove_edge(e)
