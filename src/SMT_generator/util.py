import random

from SMT_generator.scanner import ALPHABET
from SMT_generator.ast import ConcatNode, ReConcatNode
from SMT_generator.ast_walker import ASTWalker
from SMT_generator.ast import *
import SMT_generator.smt as smt
import SMT_generator.ast as sast
from SMT_generator.types import OP_TYPE
import re
import copy
from SMT_generator.generator import generate
__all__ = [
    'coin_toss',
    'random_string',
    'join_terms_with',
    'all_same',
]

# public API
def coin_toss():
    return random.choice([True, False])

def random_string(length):
    if length > 0:
        return ''.join(random.choice(ALPHABET) for i in range(length))
    else:
        return ''

def join_terms_with(terms, concatenator):
    assert len(terms) > 0

    # initialise result to the last term (i.e. first in reversed list)
    reversed_terms = reversed(terms)
    result         = next(reversed_terms)

    # keep appending preceding terms to the result
    for term in reversed_terms:
        result = concatenator(term, result)

    return result

# CREDIT:
#        https://stackoverflow.com/questions/3844801/check-if-all-elements-in-a-list-are-identical
def all_same(lst):
    return not lst or lst.count(lst[0]) == len(lst)

class VarWalker(ASTWalker):
    def __init__(self, ast, replace=None):
        super().__init__(ast)
        self.var_nodes = set()
    def exit_identifier(self, identifier, parent):
        if isinstance(identifier, VarNode) or isinstance(identifier, ConstVarNode):
            # print(identifier, ':', identifier.sort)
            self.var_nodes.add(identifier)



class changeVarWalker(ASTWalker):
    def __init__(self, ast, replace, var_set):
        super().__init__(ast)
        self.var_nodes = set()
        self.replace = replace
        self.var_dict = var_set
    def exit_identifier(self, identifier, parent):
        # print(self.var_dict)
        if isinstance(identifier, VarNode) or isinstance(identifier, ConstVarNode):
            # print(identifier, ':', identifier.sort)
            if identifier.name in self.var_dict.keys():
                identifier.name = self.var_dict[identifier.name]

class opWalker(ASTWalker):
    def __init__(self, ast):
        super().__init__(ast)
        self.op = set()
        self.string_ops =  ['Concat', 'Contains', 'At', 'Length', 'IndexOf2', 'PrefixOf', 'SuffixOf', 'Replace', 'ReInter', 'ReRange', 'RePlus', 'ReStar', 'ReConcat', 'Str2Re', 'InRegex', 'ToInt', 'Substring']

    def exit_expression(self, expression, parent):
        if any([isinstance(expression, C) for C in OP_TYPE]):
            self.op.add(expression.get_symbol())

def get_vars(newsmt):
    walker = VarWalker(newsmt)
    walker.walk()
    variables = list(walker.var_nodes)
    return variables

def make_declare(value):
    new = []
    for v in value:
        if isinstance(v, sast.AssertNode):
            new.append(v)
    declaration = []
    # print(value)
    ast_value = get_vars(new)
    for a in ast_value:
        # print(a)
        if isinstance(a, VarNode):
            declaration.append(smt.smt_declare_var(a, a.sort))
        elif isinstance(a, ConstVarNode):
            declaration.append(smt.smt_declare_const(a, a.sort))
    # print('make declare:', declaration)
    return declaration
def get_op(presmt):
    newsmt = copy.deepcopy(presmt)
    walker = opWalker(newsmt)
    walker.walk()
    operator = list(walker.op)
    return operator

def replace_var(pre_smt, replace, is_copy=True):
    var_set = {}
    if is_copy:
        newsmt = copy.deepcopy(pre_smt)
    else:
        newsmt = pre_smt
    # print('before change:\n', generate(newsmt))

    ast_var = get_vars(newsmt)
    # print('ast_var:', ast_var)
    for var in ast_var:
        var_set[var.name] = replace + str(len(var_set))
    # print('var_set:', var_set)
    walker = changeVarWalker(newsmt, replace, var_set)
    walker.walk()
    # print('after_change:\n', generate(newsmt))
    return newsmt