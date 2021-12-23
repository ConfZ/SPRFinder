import SMT_generator.generators.myGenerators as MG
from SMT_generator.generators.utils import *
import SMT_generator.generators.globalVal as g
import SMT_generator.smt as smt
import SMT_generator.ast as sast
import string
import random
import SMT_generator.generator as generator
from SMT_generator.constants import SMT_25_STRING
import time
import os
import pandas as pd

RETURN_BOOL = [
    PrefixOfNode,
    SuffixOfNode,
    ContainsNode,
    AndNode,
    OrNode,
    EqualNode,
    # NotNode,
    GtNode,
    LtNode,
    GteNode,
    LteNode,
]
RETURN_BOOL_WEIGHT = [2, 2, 2, 3, 3, 3, 1, 1, 1, 1, 1]
DECLARABLE_SORTS = [
    STRING_SORT,
    INT_SORT,
    BOOL_SORT,
]

RETURN_STRING = [
    StringReplaceNode,
    SubstringNode,
    AtNode,
    ConcatNode,
]
RETURN_STRING_WEIGHT = [4, 2, 1, 5]
RETURN_INT = [
    LengthNode,
    # IndexOfNode,
    IndexOf2Node,
]
RETURN_INT_WEIGHT = [1, 1]
sort_dict = {
    STRING_SORT: RETURN_STRING,
    INT_SORT: RETURN_INT,
    BOOL_SORT: RETURN_BOOL,
}
TERMINATION = {
    GtNode: MG.Gt_termination,
    LtNode: MG.Lt_termination,
    GteNode: MG.Gte_termination,
    LteNode: MG.Lte_termination,
    PrefixOfNode: MG.prefixof_termination,
    SuffixOfNode: MG.suffix_termination,
    ContainsNode: MG.contains_termination,
    LengthNode: MG.length_termination,
    # IndexOfNode: MG.index_termination,
    IndexOf2Node: MG.indexof2_termination,
    StringReplaceNode: MG.replace_termination,
    SubstringNode: MG.substring_termination,
    # AtNode: MG.at_termination,
    ConcatNode: MG.concat_termiatnion,
}

# RE_OPERATIONS = [
#
#
#
#
#     InReNode,
#     ReStarNode,
#     RePlusNode,
#     FromIntNode,
#     ToIntNode,
#
#     ReConcatNode,
#
#     ReUnionNode,
#     ReInterNode,
# ]

GENERATORS = {
    # NotNode: not_generator,
    AtNode: MG.At_generator,
    GtNode: MG.Gt_generator,
    GteNode: MG.Gte_generator,
    LtNode: MG.Lt_generator,
    LteNode: MG.Lte_generator,
    ContainsNode: MG.contains_generator,
    # IndexOfNode: MG.indexof_generator,
    IndexOf2Node: MG.indexof2_generator,
    PrefixOfNode: MG.prefixof_generator,
    SuffixOfNode: MG.suffixof_generator,
    StringReplaceNode: MG.replace_generator,
    ConcatNode: MG.concat_generator,
    SubstringNode: MG.substring_generator,
    AndNode: MG.and_generator,
    OrNode: MG.or_generator,
    EqualNode: MG.equal_generator,
    LengthNode: MG.length_generator,
}

def get_all_returning(sort, operations):
    return list(filter(lambda node: node.returns(sort), operations))


def termination_choices(sort):
    global TERMINATION
    terminations = get_all_returning(sort, list(TERMINATION.keys()))
    op = random.choice(terminations)
    termination = TERMINATION[op]
    expression, model = termination()
    return expression, model


def make_random_expression(sort, depth):
    # print('sort:', sort)
    sort_set = sort_dict[sort]
    if depth < 1:
        expression, model = termination_choices(sort)

        return expression, model
    random_shrunk = random.randint(0, depth - 1)
    candidate_expression = random.choice(sort_set)
    signature = candidate_expression.get_signature()
    num_args = len(signature)
    if candidate_expression is EqualNode:
        target_sort = random.choice(DECLARABLE_SORTS)
        signature = [target_sort for _ in range(num_args)]
    expressions = []
    models = []
    # print('signature:', signature)
    for sig in signature:
        expr, model = make_random_expression(sig, random_shrunk)
        expressions.append(expr)
        models.append(model)
    generator = GENERATORS[candidate_expression]
    result_expression, result_model = generator(expressions, models)

    return result_expression, result_model


def generate_assert(depth):
    expression, model = make_random_expression(BOOL_SORT, depth)
    return AssertNode(expression)


def init():
    smt.var_counter = 0
    g.var_num = 0
    g.sub_str_counter = 0
    g.var_dict = {}
    g.assem_dict = {}
    g.flag_dict = {}
    g.var_assem_dict = {}
    g.var_flag_dict = {}
    g.sub_str_counter += 1
    g.assem_dict['lit0'] = ''
    add_flag('lit0')
    # print(g.max_lit_num)
    MG.make_assemble_Str(g.max_lit_num - 1)
    # print(len(g.assem_dict))
    # new_lits = [[v] for v in list(g.assem_dict.keys())]
    # MG.make_var_pairs(len(g.assem_dict), sort = STRING_SORT, body=new_lits)


def add_const(num):
    expr = []
    assert num < len(g.var_dict), 'num must smaller than variable number'
    rand_var = random.choices(list(g.var_dict.keys()), k=num)
    for v in rand_var:
        expr.append(AssertNode(smt.smt_equal(v, g.var_dict[v])))
    return expr


def add_length(num=-1):
    expr = []
    all_str_var = get_str_vars()
    assert num < len(all_str_var), 'num must smaller than variable number'
    if num == -1:
        for v in all_str_var:
            text = get_text(v)
            expr.append(AssertNode(smt.smt_equal(smt.smt_len(v), smt.IntLitNode(len(text)))))
    elif num == 0:
        return []
    else:
        weights = [g.var_flag_dict[v] for v in all_str_var]
        random_var = random.choices(all_str_var, weights=weights, k=num)
        for v in random_var:
            text = get_text(v)
            expr.append(AssertNode(smt.smt_equal(smt.smt_len(v), smt.IntLitNode(len(text)))))
    return expr


def make_random_ast(num_vars, num_asserts, depth, max_str_length, max_int_length,
                    new_var_probability, const_num, length_num, is_shark="Off"):
    if (depth > g.max_depth):
        depth = g.max_depth
    init()
    g.max_var_number = num_vars
    g.max_lit_length = max_str_length
    g.max_int_lit = max_int_length
    g.is_shark = is_shark
    g.new_variable_probability = new_var_probability
    asserts = [generate_assert(depth) for _ in range(num_asserts)]
    const_eql = add_const(const_num)
    asserts = asserts + const_eql
    asserts = asserts + add_length(length_num)

    declarations = []
    str_vars = get_str_vars()
    int_vars = get_int_vars()
    bool_vars = get_bool_vars()

    for s in str_vars:
        declarations.append(smt.smt_declare_var(s, sort='String'))
    for s in int_vars:
        declarations.append(smt.smt_declare_var(s, sort='Int'))
    for s in bool_vars:
        declarations.append(smt.smt_declare_var(s, sort='Bool'))
    expressions = asserts + [CheckSatNode()]
    declarations = [smt.smt_string_arithmatic_logic()] + declarations
    return declarations + expressions


if __name__ == "__main__":
    i = 0
    NAME = []
    RESULT = []
    TIME = []
    while i < 1000:
        file_name = 'test' + str(i)
        NAME.append(file_name)
        expr = make_random_ast(
            num_vars=15,
            num_asserts=10,
            max_str_length=20,
            max_int_length=random.randint(10, 20),
            depth=2,
            new_var_probability=0.7,
            const_num=3,
            length_num=random.randint(0, 3),
            is_shark='Off'
        )
        print('files number:', i)
        name = r'/home/zy/Documents/benchmarks/short_length/' + file_name + '.smt2'
        generator.generate_file(expr, SMT_25_STRING, name)
        i += 1
