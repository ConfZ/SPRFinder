'''
The bandit transformer takes in an instance and an operator, and inserts a new 
occurence of the operator into the instance.
'''

import sys

import random

from SMT_generator.types import STR_RET, INT_RET, BOOL_RET, RX_RET
from SMT_generator.ast_walker import ASTWalker
from SMT_generator.smt import smt_declare_var
from SMT_generator.ast import FunctionDeclarationNode, ConstantDeclarationNode

from SMT_generator.generators.random_ast import make_random_expression, VarNode
ALL_SUPPORTED = STR_RET + INT_RET + BOOL_RET + RX_RET
OPERATORS = [x.get_symbol() for x in ALL_SUPPORTED]

__all__ = [
    'bandit',
]

class BanditTransformer(ASTWalker):
    def __init__(self, ast, pair):
        super().__init__(ast)
        self.pair = pair
        self.replaced = False

    def enter_expression(self, expr, parent):
        if self.replaced:
            return
        for i in range(len(expr.body)):
            if expr.body[i] == self.pair[0]:
                expr.body[i] = self.pair[1]
                self.replaced = True


class BanditFinder(ASTWalker):
    def __init__(self, ast, op):
        super().__init__(ast)
        self.op     = op
        self.target = None
        self.variables = set()
        self.exists = False
        self.defs = {}

    def exit_identifier(self, identifier, parent):
        if isinstance(identifier, VarNode):
            self.variables.add(identifier)
            sort = identifier.sort
            # if sort not in self.variables.keys():
            #     self.variables[sort] = []
            # if identifier not in self.variables[sort]:
            #     self.variables[sort].append(identifier)
        # print(self.defs)
        # sort = self.defs[identifier.name]
        # if sort not in self.variables:
        #     self.variables[sort] = []
        #
        # if identifier not in self.variables[sort]:
        #     self.variables[sort].append(identifier)

    def enter_expression(self, expr, parent):
        # if isinstance(expr, FunctionDeclarationNode):
        #     ident = expr.body[0].name
        #     sort = expr.body[2].name
        #     self.defs[ident] = sort
        #     return
        #
        # if isinstance(expr, ConstantDeclarationNode):
        #     ident = expr.body[0].name
        #     sort = expr.body[1].name
        #     self.defs[ident] = sort
        #     return

        replace = random.choice([True, False])
        if self.op.get_symbol() == expr.get_symbol():
            return
        if self.op in STR_RET and any([isinstance(expr, C) for C in STR_RET]):
            self.exists = True
            if replace:
                self.target = expr
        elif self.op in INT_RET and any([isinstance(expr, C) for C in INT_RET]):
            self.exists = True
            if replace:
                self.target = expr
        elif self.op in BOOL_RET and any([isinstance(expr, C) for C in BOOL_RET]):
            self.exists = True
            if replace:
                self.target = expr
        elif self.op in RX_RET and any([isinstance(expr, C) for C in RX_RET]):
            self.exists = True
            if replace:
                self.target = expr

def find_node(op):
    for node in ALL_SUPPORTED:
        if node.get_symbol() == op:
            return node
    return None


def gen_pair(op_node, old_expr, variables, depth):
    sig = op_node.get_signature()
    old_sig = old_expr.get_signature()
    args = []
    new_vars = []
    for j in range(len(sig)):
        s = sig[j]
        found = False
        for i in range(len(old_sig)):
            index = (i+j) % len(old_sig)
            if old_sig[index] == s:
                e = old_expr.body[index]
                args.append(e)
                found = True
                break
        if not found:
            is_exist = False
            for v in variables:
                if v.sort == s:
                    is_exist = True
            if not is_exist:
                it = len(variables)
                new_var = VarNode('newVar' + str(it + 1), s)
                new_vars.append(new_var)
                variables.append(new_var)
            args.append(make_random_expression(variables, s, depth, True))

    return [old_expr, op_node(*args)], new_vars

# public API
def bandit(ast, op, depth):

    tmp = find_node(op)
    if tmp is None:
        print("NOT SUPPORTED: " + op, file=sys.stderr)
        return ast 

    op = tmp
    finder = BanditFinder(ast, op)

    while finder.target == None:
        finder.walk()
        if not finder.exists:
            return ast
    print('finder.varibles:', finder.variables)
    pair, new_vars = gen_pair(op, finder.target, list(finder.variables), depth)
    transformed = BanditTransformer(ast, pair).walk()
    for v in new_vars:
        transformed = [smt_declare_var(v, v.sort)] + transformed
    return transformed
