from utils import *


def rule1(id, exp):
    """
    PUSH Imm / POP Reg  <-->  MOV Reg,Imm
    """
    if exp:    # expansion
        if program[id][0] == "mov":  # is exactly a mov instruction
            if (itype(program[id][1]) == 0) & (itype(program[id][2]) == 2):  # operand 1 is a register and 2 immediate
                    istr1 = ["push", program[id][2]]
                    istr2 = ["pop", program[id][1]]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:   # compression
        if id != len(program)-1:    # checking if id is not the last istruction of the program
            if (program[id][0] == "push") & (program[id+1][0] == "pop"):
                if (itype(program[id][1]) == 2) & (itype(program[id+1][1]) == 0):
                    istr = ["mov", program[id+1][1], program[id][1]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule2(id, exp):
    """
    PUSH Reg / POP Reg2  <-->  MOV Reg2,Reg
    """
    if exp:
        if program[id][0] == "mov":
            if (itype(program[id][1]) == 0) & (itype(program[id][2]) == 0):
                    istr1 = ["push", program[id][2]]
                    istr2 = ["pop", program[id][1]]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "push") & (program[id+1][0] == "pop"):
                if (itype(program[id][1]) == 0) & (itype(program[id+1][1]) == 0) & (program[id][1] != program[id+1][1]):
                    istr = ["mov", program[id+1][1], program[id][1]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule3(id, exp):
    """
    MOV Mem,Imm / PUSH Mem	<-->  PUSH Imm
    """
    if exp:
        if program[id][0] == "push":
            if itype(program[id][1]) == 2:
                    m = randomMem()
                    istr1 = ["mov", m, program[id][1]]
                    istr2 = ["push", m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (program[id+1][0] == "push"):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) == 2) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["push", program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule4(id, exp):
    """
    MOV Mem,Reg / PUSH Mem   <-->  PUSH Reg
    """
    if exp:
        if program[id][0] == "push":
            if itype(program[id][1]) == 0:
                    m = randomMem()
                    istr1 = ["mov", m, program[id][1]]
                    istr2 = ["push", m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (program[id+1][0] == "push"):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) == 0) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["push", program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule5(id, exp):
    """
    POP Mem2 / MOV Mem,Mem2	<-->  POP Mem
    """
    if exp:
        if program[id][0] == "pop":
            if itype(program[id][1]) == 1:
                    m = randomMem()
                    istr1 = ["pop", m]
                    istr2 = ["mov", program[id][1], m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "pop") & (program[id+1][0] == "mov"):
                if (itype(program[id][1]) == 1) & (itype(program[id+1][1]) == 1) & (itype(program[id+1][2]) == 1) & (program[id][1] == program[id+1][2]) & (program[id][1] != program[id+1][1]):
                    istr = ["pop", program[id+1][1]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule6(id, exp):
    """
    POP Mem / MOV Reg,Mem  <-->  POP Reg
    """
    if exp:
        if program[id][0] == "pop":
            if itype(program[id][1]) == 0:
                    m = randomMem()
                    istr1 = ["pop", m]
                    istr2 = ["mov", program[id][1], m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "pop") & (program[id+1][0] == "mov"):
                if (itype(program[id][1]) == 1) & (itype(program[id+1][1]) == 0) & (itype(program[id+1][2]) == 1) & (program[id][1] == program[id+1][2]):
                    istr = ["pop", program[id+1][1]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule7(id, exp):
    """
    MOV Mem,Imm / OP Reg,Mem  <-->  OP Reg,Imm
    """
    if exp:
        if len(program[id]) == 3:
            if (itype(program[id][1]) == 0) & (itype(program[id][2]) == 2):
                    m = randomMem()
                    istr1 = ["mov", m, program[id][2]]
                    istr2 = [program[id][0], program[id][1], m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (len(program[id+1]) == 3):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) == 2) & (itype(program[id+1][1]) == 0) & (itype(program[id+1][2]) == 1) & (program[id][1] == program[id+1][2]):
                    istr = [program[id+1][0], program[id+1][1], program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule8(id, exp):
    """
    MOV Mem2,Mem / OP Reg,Mem2  <-->  OP Reg,Mem
    """
    if exp:
        if len(program[id]) == 3:
            if (itype(program[id][1]) == 0) & (itype(program[id][2]) == 1):
                    m = randomMem()
                    istr1 = ["mov", m, program[id][2]]
                    istr2 = [program[id][0], program[id][1], m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (len(program[id+1]) == 3):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) == 1) & (itype(program[id+1][1]) == 0) & (itype(program[id+1][2]) == 1) & (program[id][1] == program[id+1][2]):
                    istr = [program[id+1][0], program[id+1][1], program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule9(id, exp):
    """
    POP Mem / PUSH Mem  <-->  NOP
    """
    if exp:
        if program[id][0] == "nop":
            m = randomMem()
            istr1 = ["pop", m]
            istr2 = ["push", m]
            program.pop(id)
            program.insert(id, istr2)
            program.insert(id, istr1)
            return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "pop") & (program[id+1][0] == "push"):
                if (itype(program[id][1]) == 1) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["nop"]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule10(id, exp):
    """
    MOV Mem,Reg / CALL Mem  <-->  CALL Reg
    """
    if exp:
        if program[id][0] == "call":
            if itype(program[id][1]) == 0:
                    m = randomMem()
                    istr1 = ["mov", m, program[id][1]]
                    istr2 = ["call", m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (program[id+1][0] == "call"):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) == 0) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["call", program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule11(id, exp):
    """
    MOV Mem2,Mem / CALL Mem2  <-->  CALL Mem
    """
    if exp:
        if program[id][0] == "call":
            if itype(program[id][1]) != 0:
                    m = randomMem()
                    istr1 = ["mov", m, program[id][1]]
                    istr2 = ["call", m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (program[id+1][0] == "call"):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) != 0) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["call", program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule12(id, exp):
    """
    MOV Mem,Reg / JMP Mem  <-->  JMP Reg
    """
    if exp:
        if program[id][0] == "jmp":
            if itype(program[id][1]) == 0:
                    m = randomMem()
                    istr1 = ["mov", m, program[id][1]]
                    istr2 = ["jmp", m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (program[id+1][0] == "jmp"):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) == 0) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["jmp", program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule13(id, exp):
    """
    PUSH Reg / RET  <-->  JMP Reg
    """
    if exp:
        if program[id][0] == "jmp":
            if itype(program[id][1]) == 0:
                    istr1 = ["push", program[id][1]]
                    istr2 = ["ret"]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "push") & (program[id+1][0] == "ret"):
                if itype(program[id][1]) == 0:
                    istr = ["jmp", program[id][1]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule14(id, exp):
    """
    MOV Mem2,Mem / JMP Mem2  <-->  JMP Mem
    """
    if exp:
        if program[id][0] == "jmp":
            if itype(program[id][1]) != 0:
                    m = randomMem()
                    istr1 = ["mov", m, program[id][1]]
                    istr2 = ["jmp", m]
                    program.pop(id)
                    program.insert(id, istr2)
                    program.insert(id, istr1)
                    return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "mov") & (program[id+1][0] == "jmp"):
                if (itype(program[id][1]) == 1) & (itype(program[id][2]) != 0) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["jmp", program[id][2]]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def rule15(id, exp):
    """
    POP Mem / JMP Mem  <-->  RET
    """
    if exp:
        if program[id][0] == "ret":
            m = randomMem()
            istr1 = ["pop", m]
            istr2 = ["jmp", m]
            program.pop(id)
            program.insert(id, istr2)
            program.insert(id, istr1)
            return True
    else:
        if id != len(program) - 1:
            if (program[id][0] == "pop") & (program[id+1][0] == "jmp"):
                if (itype(program[id][1]) == 1) & (itype(program[id+1][1]) == 1) & (program[id][1] == program[id+1][1]):
                    istr = ["ret"]
                    program.pop(id)
                    program.pop(id)
                    program.insert(id, istr)
                    return True
    return False


def spec_rule1(id, exp):
    """
    PUSH T / POP T <-- MOV T,T
    """
    if program[id][0] == "mov":
        istr1 = ["push", program[id][2]]
        istr2 = ["pop", program[id][1]]
        program.pop(id)
        program.insert(id, istr2)
        program.insert(id, istr1)
        return True
    return False


def spec_rule2(id, exp):
    """
    MOV T,T / PUSH T <-- PUSH T
    """
    if program[id][0] == "push":
        istr1 = ["mov", "T", program[id][1]]
        istr2 = ["push", "T"]
        program.pop(id)
        program.insert(id, istr2)
        program.insert(id, istr1)
        return True
    return False


def spec_rule3(id, exp):
    """
    POP T / MOV T,T <-- POP T
    """
    if program[id][0] == "pop":
        istr1 = ["pop", "T"]
        istr2 = ["mov", program[id][1], "T"]
        program.pop(id)
        program.insert(id, istr2)
        program.insert(id, istr1)
        return True
    return False


rules = [0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9]  # only rules from 1 to 9 are used
# rules = [0, spec_rule1, spec_rule2, spec_rule3]
# rules = [0, rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15]
