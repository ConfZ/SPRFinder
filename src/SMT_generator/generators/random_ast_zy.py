import random
import inspect

from SMT_generator.ast import *
import SMT_generator.smt as smt
from SMT_generator.smt import smt_reset_counters, smt_declare_var
from SMT_generator.util import random_string, coin_toss
import SMT_generator.generators.globalVal as g

__all__ = [
    'random_ast'
]

# constants
# nodes that have no inputs
TERMINALS = [
    ReAllCharNode,
]

# nodes that can take expressions
NONTERMINALS = [
    NotNode,
    GtNode,
    LtNode,
    GteNode,
    LteNode,
    ContainsNode,
    AtNode,
    LengthNode,
    # IndexOfNode,
    IndexOf2Node,
    PrefixOfNode,
    SuffixOfNode,
    StringReplaceNode,
    SubstringNode,
    InReNode,
    ReStarNode,
    RePlusNode,
    # FromIntNode,
    ToIntNode,
]

# nodes that can take only terminals
ALMOST_TERMINALS = [
    StrToReNode,
    ReRangeNode,
]

N_ARY_NONTERMINALS = [
    ConcatNode,
    ReConcatNode,
    AndNode,
    OrNode,
    EqualNode,
    ReUnionNode,
    ReInterNode,
]
NONTERM = NONTERMINALS + N_ARY_NONTERMINALS
EXPRESSION_SORTS = DECLARABLE_SORTS + [REGEX_SORT]

# global config
# max values
_max_terms = 0
_max_str_lit_length = 0
_max_int_lit = 0
_max_var_num = 0
_max_depth = 4
_max_int_var = 4
_max_bool_var = 4
max_len = 0
# min values
_min_var_num = 1
_min_terms = 4
_min_int_lit = 0
_min_str_lit = 0

_literal_probability = 0.0
_semantically_valid = False
_new_var_probability = 0.0
_var_num = 0


# list
flag_dict = {}
# variables
variables = []
sort_num = {}
non_term_weight = {}


# helpers
def get_all_returning_a(sort, nodes):
    return list(filter(lambda node: node.returns(sort), nodes))


def get_terminals(nodes):
    return filter(lambda node: node.is_terminal(), nodes)


def make_random_literal(sort):
    if sort == STRING_SORT:
        global max_len
        str_len = random.randint(_min_str_lit, _max_str_lit_length)
        if str_len > max_len:
            max_len = str_len
        return StringLitNode(random_string(str_len))

    if sort == INT_SORT:
        return IntLitNode(random.randint(_min_int_lit, _max_int_lit))

    if sort == BOOL_SORT:
        return BoolLitNode(coin_toss())

    raise ValueError('unknown sort {}'.format(sort))


def should_choose_literal():
    global _literal_probability
    return random.random() < _literal_probability


def _get_weight(v, max_num, shark='Off'):
    global flag_dict
    if isinstance(v, VarNode):
        weight_value = flag_dict[v]
    else:
        raise ValueError('unknown sort {}'.format(type(v)))
    if shark == 'Off':
        w = max_num - weight_value
    else:
        w = weight_value
    if w < 1:
        w = 1
    return w


def make_random_terminal(sort):
    global _str_var_num, _int_var_num, _bool_var_num, _new_var_probability, _min_var_num, _max_var_num
    if sort == REGEX_SORT:
        return ReAllCharNode()

    # randomly choose between a variable or a literal
    if should_choose_literal():
        return make_random_literal(sort)
    cand_var = []
    global variables, sort_num
    if sort_num[sort] <= _min_var_num or (random.random() < _new_var_probability and len(variables) <= _max_var_num) :
        new_var = VarNode(smt.new_var(), sort)
        # print(type(variables))
        variables.append(new_var)
        flag_dict[new_var] = 1
        sort_num[sort] += 1
        return new_var
    else:
        for v in variables:
            if v.sort == sort:
                cand_var.append(v)
        # print('min_var:', _min_var_num)
        # print('max_var:', _max_var_num)
        # print('cand_var:', cand_var)
        weight = [_get_weight(v, sort_num[sort]) for v in cand_var]
        # print('weight：', weight)
        # print(sort, ':', sort_num[sort])
        target_var = random.choices(cand_var, weights=weight, k=1)[0]
        flag_dict[target_var] += 1
        return target_var


def make_random_expression(sort, depth, valid_override=False):
    global _semantically_valid

    # if semantics are going to hell, then randomly reinvent the sort
    # if _semantically_valid is False and valid_override is False:
    #     sort = random.choice(EXPRESSION_SORTS)

    # at depth 0, make a terminal
    if depth < 1:
        return make_random_terminal(sort)

    # randomly shrink the depth
    shrunken_depth = random.randint(0, depth - 1)

    # get random expression generator
    candidate_nodes = get_all_returning_a(sort, NONTERMINALS)

    global non_term_weight
    weight = [non_term_weight[v] for v in candidate_nodes]
    # print(weight)
    expression_node = random.choices(candidate_nodes, weights=weight, k=1)[0]
    if expression_node == IndexOfNode:
        signature = expression_node.get_signature()
    else:

        signature = expression_node.get_signature()
    num_args = len(signature)

    # if the expression takes any sort, pick one
    if expression_node.accepts(ANY_SORT):
        collapsed_sort = random.choice(DECLARABLE_SORTS)
        signature = [collapsed_sort for i in range(num_args)]

    # generate random arguments
    random_args = [make_random_expression(arg_sort, shrunken_depth, valid_override) for arg_sort in
                   signature]

    # build expression
    expression = expression_node(*random_args)

    return expression


def generate_assert(depth):
    expression = make_random_expression(BOOL_SORT, depth)
    return AssertNode(expression)


def init():
    global _var_num, flag_dict, variables
    smt.var_counter = 0
    _var_num = 0
    sort_num[INT_SORT] = 0
    sort_num[STRING_SORT] = 0
    sort_num[BOOL_SORT] = 0
    flag_dict = {}
    variables = []


def make_random_ast(max_var_num, max_terms, max_depth, max_str_lit_length, max_int_lit, literal_probability,
                    semantically_valid, new_var_probability=0.7, op_weight=None, min_var_num=3, min_terms=4, min_str_lit=10, min_int_lit=0):
    if op_weight is None:
        op_weight = []
    init()
    global _max_terms
    global _max_str_lit_length
    global _max_int_lit
    global _literal_probability
    global _semantically_valid
    global _max_var_num, _max_depth, _min_var_num, _min_terms, _new_var_probability, max_len
    # set global config
    # max config
    _max_terms = max_terms
    _max_str_lit_length = max_str_lit_length
    _max_int_lit = max_int_lit
    _max_var_num = max_var_num
    _literal_probability = literal_probability
    _new_var_probability = new_var_probability
    max_len = 0

    _semantically_valid = semantically_valid

    # min config

    _min_var_num = min_var_num
    _min_terms = min_terms
    _min_str_lit = min_str_lit
    _min_int_lit = min_int_lit

    # weight
    global non_term_weight
    for t in NONTERMINALS:
        non_term_weight[t] = 1
    if len(op_weight) != 0:
        for op in op_weight:
            for non_op in non_term_weight:
                if non_op.get_symbol() == op:
                    non_term_weight[non_op] += op_weight[op]
    for s in DECLARABLE_SORTS:
        sort_num[s] = 0

    num_asserts = random.randint(_min_terms, _max_terms)
    asserts = [generate_assert(max_depth) for i in range(num_asserts)]
    # create declarations
    declarations = []
    # for s in DECLARABLE_SORTS:
    #     new_declarations = [smt_declare_var(v, sort=s) for v in variables[s]]
    #     declarations.extend(new_declarations)
    for v in variables:
        new_decalration = smt_declare_var(v, v.sort)
        declarations.append(new_decalration)
    # create asserts

    # add check-sat
    expressions = asserts + [CheckSatNode()]

    return declarations + expressions, [len(variables), num_asserts, max_len, max_depth]


# public API
def random_ast(*args, **kwargs):
    smt_reset_counters()
    return make_random_ast(*args, **kwargs)
