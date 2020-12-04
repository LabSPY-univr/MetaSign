#!/usr/bin/python3
from rulesDef import *
from rulesInfer import *
import sys
import getopt


def applyRule(exp, rule, ppoint):
    """
    Apply rule to program point ppoint as expansion(exp=1) or compression(exp=0)
    :param exp: if 1 then expansion otherwise compression
    :param rule: index indicating which rules to apply
    :param ppoint: program point from which try to apply rule
    :return: -1 if could not apply the rule to any program point
    """
    new_p = ppoint
    while not rules[rule](new_p, exp):
        new_p = (new_p + 1) % len(program)
        if new_p == ppoint:  # if True then couldn't apply the rule to any instruction
            return -1
    return new_p


def read_assembly(name):
    """
    Read and parse the file name saving all instructions to program
    :param name: name of the file containing the instructions
    :return: None
    """
    program.clear()
    try:
        file = open(name)
    except IOError:
        print("Error: file ", name, " does not exist")
        sys.exit()
    for line in file:
        line = line.replace(',', '')
        line.lower()
        if (len(line) > 2) & ("Applied" not in line):
            program.append(line.split())
    file.close()


def writeProgram(filename, exp, rule, ppoint):
    """
    write current instructions in variable program to file
    :param filename: name of the file
    :param exp: if 1 then expansion was applied otherwise compression
    :param rule: which rule was applied
    :param ppoint: on which program point was applied
    :return: None
    """
    f = open(filename, 'w')
    if debug:
        print()
        print(program)
        print("Applied rule number", rule)
        print("Applied as ", end="")
    if exp == 0:
        exp_s = "Compression rule"
        if debug:
            print("Compression rule")
    else:
        exp_s = "Expansion rule"
        if debug:
            print("Expansion rule")
    if debug:
        print("To program point", ppoint)
    for i in range(0, len(program)):
        if len(program[i]) == 2:
            s = program[i][0] + ' ' + program[i][1]
        elif len(program[i]) == 3:
            s = program[i][0] + ' ' + program[i][1] + ', ' + program[i][2]
        else:
            s = program[i][0]
        f.write(s)
        f.write('\n')
    f.write('\n')
    f.write('\n')
    s = "Applied rule number " + str(rule) + " as " + exp_s + " to program point " + str(ppoint)
    f.write(s)
    f.flush()
    f.close()


def help():
    """
    Print -h parameter
    :return: None
    """
    print("""
        Author: Marco Campion vr383227 University of Verona

        meta.py: metamorphic engine and widening on programs as automata

        Usage: python meta.py [-h][-w][-e][-v][-s][-n <number>][-r][-i <variant1,variant2,...>][-l <number>] <first_program>

        -h (help) print this message
        -w widening on variants will be applied
        -e (expansion) only expansion rules will be used
        -v (verbose) all passes of widening will be showed
        -s (silence) no prints will be output
        -n <number> the number of variants to be generated
        -r (rewriting rules) try to infer rewriting rules from variants specified with param. -i
        -i <variant1,variant2,...> all the variants to be widened together with the origin program (comma separated and no spaces)
        -l <number> the length of the language of each node in CFG (default is 2)
        <first_program> the origin program from which to start generating the variants or the widening
        """)


# PROGRAM EXECUTION STARTS HERE
# checking arguments
variants = 0
N_lang = 2
metamorphic_engine = False  # if True variants will be generated from first program
widening = False  # if True the wdn will be applied to either variants generated or variants given in input
expansion = False  # if True only expansion rules will be applied
verbose = False  # if True all passes of widening will be showed
silence = False  # if True no prints will be done
debug = False  # if True, rules applied will be printed
rewriting_rules = False  # if True, try to infer rewriting rules from variants
inputfiles = []
if len(sys.argv) == 1:
    print("Error: no assembly file as input")
    sys.exit()
try:
    opts, args = getopt.getopt(sys.argv[1:],"hwvesdrl:n:i:")
except getopt.GetoptError:
    print("Error: parameters incorrect")
    help()
    sys.exit()
for opt, arg in opts:
    if opt == '-h':
        help()
        sys.exit()
    elif opt == '-w':
        widening = True
    elif opt == '-e':
        expansion = True
    elif opt == '-v':
        verbose = True
        silence = False
    elif opt == '-s':
        silence = True
        verbose = False
        debug = False
    elif opt == '-d':
        debug = True
        verbose = True
        silence = False
    elif opt == '-r':
        rewriting_rules = True
    elif opt == '-i':
        widening = True
        metamorphic_engine = False
        if len(arg) < 1:
            help()
            print("Error: no input after -i")
            sys.exit()
        inputfiles = arg.split(',')
        variants = len(inputfiles)
    elif opt == '-n':
        if len(arg) < 1:
            help()
            print("Error: no input after -n")
            sys.exit()
        try:
            variants = int(arg)
        except ValueError:
            print("Error: value after -n must be a number")
            sys.exit()
        metamorphic_engine = True
    elif opt == '-l':
        if len(arg) < 1:
            help()
            print("Error: no input after -l")
            sys.exit()
        try:
            N_lang = int(arg)
        except ValueError:
            print("Error: value after -l must be a number")
            sys.exit()

# parsing assembly file
read_assembly(args[0])

# generating control flow graph and the language for current program before generating the variant/doing the wdn.
# First program will be the first graph for widening
if not silence:
    print()
    print("-- PROGRAM --")
    print(program)
if widening:
    # generating the graph, language and abstraction of the starting program
    genGraph(graph_wdn, mark_wdn)
    if verbose:
        print()
        print("dict_graph")
        print(dict_graph)
        print()
        print("lang")
    genLang(N_lang, graph_wdn, lang_wdn)
    if verbose:
        printLang(graph_wdn, lang_wdn)
        print()
    setAbstraction(graph_wdn, abs_ins_wdn, vertex_name_wdn)
    if verbose:
        print("abs_program")
        printAbstraction(graph_wdn, abs_ins_wdn)
        print()
    vertex_shape_wdn.set_value("circle")
    vertex_shape_wdn[graph_wdn.vertex(0)] = "double_circle"
if rewriting_rules:
    # generating the abstract program and adding it to the positive set to analyze
    genAbstractProgram()
    positive_set.append(abstract_program.copy())

# generating the new variant/doing the wdn
g = Graph()
for i in range(1, variants+1):
    if metamorphic_engine:
        # generating random if exp/comp, which rule and from which point of program
        if not expansion:
            exp = random.randint(0, 1)
        else:
            exp = 1
        rule = random.randint(1, len(rules)-1)
        ppoint = random.randint(0, len(program)-1)

        # applying rule to instruction
        real_ppoint = applyRule(exp, rule, ppoint)
        if real_ppoint == -1 and not expansion:   # if True then try with another exp
            nstats[2] += 1
            if exp == 1:
                if debug:
                    print("changed exp from Expansion to Compression")
                exp = 0
            else:
                if debug:
                    print("changed exp from Compression to Expansion")
                exp = 1
            real_ppoint = applyRule(exp, rule, ppoint)

        while real_ppoint == -1:    # if still -1 then try with another rule
            if debug:
                print("changed rule from", rule, end=" ")
            nstats[2] += 1
            rule = random.randint(1, len(rules)-1)
            if debug:
                print("to", rule)
            real_ppoint = applyRule(exp, rule, ppoint)
            if not expansion:
                if real_ppoint != -1:
                    break
                nstats[2] += 1
                if exp == 1:
                    if debug:
                        print("changed exp from Expansion to Compression")
                    exp = 0
                else:
                    if debug:
                        print("changed exp from Compression to Expansion")
                    exp = 1
                real_ppoint = applyRule(exp, rule, ppoint)

        # fixing all jumps/calls adresses
        fixAdr(exp, real_ppoint)

        # updating stats
        if exp == 1:
            nstats[0] += 1
        else:
            nstats[1] += 1
        nrules[rule] += 1

        # writing the new variant to file
        namel = sys.argv[-1].split('.')
        name = namel[0] + str(i) + ".txt"
        writeProgram(name, exp, rule, real_ppoint)
        if not widening and not silence:
            print()
            print("-- VARIANT " + str(i) + " --")
            print(program)
    else:
        read_assembly(inputfiles[i-1])

    if rewriting_rules:
        # generating the abstract program and adding it to the positive set to analyze
        genAbstractProgram()
        if abstract_program not in positive_set:
            positive_set.append(abstract_program.copy())

    if widening:
        # generating the graph, language and abstraction of the current variant
        abs_ins_g = g.new_vertex_property("object")
        vertex_name_g = g.new_vertex_property("string")
        vertex_shape_g = g.new_vertex_property("string")
        lang_g = g.new_vertex_property("object")
        mark_g = g.new_vertex_property("bool")
        if not silence:
            print()
            print("-- VARIANT " + str(i) + " --")
            print(program)
        genGraph(g, mark_g)
        if verbose:
            print()
            print("dict_graph")
            print(dict_graph)
            print()
            print("lang")
        genLang(N_lang, g, lang_g)
        if verbose:
            printLang(g, lang_g)
            print()
        setAbstraction(g, abs_ins_g, vertex_name_g)
        if verbose:
            print("abs_program")
            printAbstraction(g, abs_ins_g)
            print()
        vertex_shape_g.set_value("circle")
        vertex_shape_g[g.vertex(0)] = "double_circle"

        # now graph variant will be inserted in graph_wdn
        graph_union(graph_wdn, g, props=[(lang_wdn, lang_g), (mark_wdn, mark_g), (abs_ins_wdn, abs_ins_g), (vertex_name_wdn, vertex_name_g), (vertex_shape_wdn, vertex_shape_g)], include=True)
        g.clear()
        lang_wdn = graph_wdn.new_vertex_property("object")
        genLang(N_lang, graph_wdn, lang_wdn)

        # marking nodes with same language
        markNodes_new(graph_wdn, mark_wdn, abs_ins_wdn, lang_wdn)
        if verbose:
            printMark_new()
            printGraph(graph_wdn, vertex_name_wdn, vertex_shape_wdn)
            print()

        # applying the widening
        for v in to_merge:
            mergeNodes(graph_wdn, v, abs_ins_wdn, vertex_name_wdn, vertex_shape_wdn)
        oldv = []
        for d in to_merge:  # remove the merged nodes
            for v in d:
                oldv.append(graph_wdn.vertex(v))
        graph_wdn.remove_vertex(oldv)

        # generating the new lang for the new wdn graph
        lang_wdn = graph_wdn.new_vertex_property("object")
        genLang(N_lang, graph_wdn, lang_wdn)
        mark_wdn = graph_wdn.new_vertex_property("bool")
        if verbose:
            printGraph(graph_wdn, vertex_name_wdn, vertex_shape_wdn)

if metamorphic_engine:
    print()
    print("Correctly generated " + str(i) + " variants!")
    print()
    stats()
if rewriting_rules:
    """
    # inferring all rules from the positive set
    print()
    print("positive_set:")
    print(positive_set)
    rules_inferred = infer(positive_set)
    print()
    if debug:
        print("Rewriting rules BEFORE semplification:")
        printRules(rules_inferred)
        print()
    # try to remove rules which can be simplified to a smaller rule
    start_simplify(rules_inferred)
    print("Rewriting rules inferred:")
    printRules(rules_inferred)
    print()
    """

    edge_visited = graph_wdn.new_edge_property("bool")  # mark all edges as not visited
    roots = getRoots(graph_wdn, vertex_shape_wdn)
    all_visited = False
    minimum = len(min(positive_set, key=len))+1  # length of first program
    maximum = len(max(positive_set, key=len))+2  # length of the biggest (more instructions) program
    positive_set.clear()
    for k in range(minimum, maximum):
        for v in roots:  # getting all paths from roots to node 'ret' of length k until all edges are visited
            all_visited = printAllPaths(graph_wdn, vertex_name_wdn, edge_visited, int(v), int(getRet(graph_wdn)), k)
            if all_visited:  # if True then all edges have been visited so no more searches are needed
                break
        if all_visited:
            break
    if debug:
        print(minimum)
        print(maximum-1)
        print(k)
        print(all_visited)
        print("positive_set:")
        print(positive_set)
    # inferring all rules from the positive set
    rules_inferred = infer(positive_set)
    print()
    if debug:
        print("Rewriting rules BEFORE semplification:")
        printRules(rules_inferred)
        print()
    # try to remove rules which can be simplified to a smaller rule
    start_simplify(rules_inferred)
    print("Rewriting rules inferred:")
    printRules(rules_inferred)
    print()

if widening:
    print()
    print("Widening done!")
    print()
    printGraph(graph_wdn, vertex_name_wdn, vertex_shape_wdn, output=True)
