import SMT_generator.smt as smt
from SMT_generator.generators.utils import *
import SMT_generator.generators.globalVal as g


def coin_toss():
    return random.choice([False, True])


def random_text(min, max):
    length = random.randint(min, max)
    return ''.join(random.choice(g.ALPHABET) for _ in range(0, length))


def new_assemble_var():
    result = 'lit{}'.format(g.sub_str_counter)
    g.sub_str_counter += 1
    return result


def make_new_lit(text, target_flag=None):
    new_lit = new_assemble_var()
    g.assem_dict[new_lit] = text
    if target_flag:
        g.flag_dict[new_lit] = target_flag
    else:
        add_flag(new_lit)
    return new_lit


def make_assemble_Str(num):
    all_str = []
    for i in range(num):
        text = random_text(g.min_lit_length, g.max_lit_length)
        assem_str = make_new_lit(text)
        all_str.append(assem_str)
    return all_str


def random_int_variable(min, max_len):
    int_vars = get_int_vars()
    if len(int_vars) is not 0 and random.random() > g.new_variable_probability:
        target_int_vars = list(filter(lambda x: min <= g.var_dict[x].value < max_len, int_vars))
        if len(target_int_vars) is not 0:
            target_var = random.choice(target_int_vars)
            return target_var
        else:
            body = random.randint(min, max_len)
            target_var = make_var_pairs(1, sort=INT_SORT, body=body)
            return target_var
    else:
        body = random.randint(min, max_len)
        target_var = make_var_pairs(1, sort=INT_SORT, body=body)
        return target_var


def make_var_pairs(vars_num, sort, body=None):
    if vars_num == 1 and body is not None:
        body = [body]
    variables = [smt.smt_new_var() for _ in range(vars_num)]
    litnodes = []
    if sort is STRING_SORT:
        if body is None:
            for var in variables:
                assem_vars = random_choose_lits(list(g.assem_dict.keys()), random.randint(1, len(g.assem_dict)))
                # print('assen_vars', assem_vars)
                # print('assem_var:', assem_vars)
                text = literals_to_text(assem_vars)
                g.var_dict[var] = smt.smt_str_lit(text)
                g.var_assem_dict[var] = assem_vars
                g.var_num += 1
                add_var_flag(var)
            assert(len(variables) is not 0)
            if vars_num == 1:
                return variables[0]
            else:
                return variables
        else:
            assert vars_num == len(body)
            # print('body:', body)
            for i in range(vars_num):
                b = body[i]
                for str in b:
                    # print('str', str)
                    add_flag(str)

                text = get_text(b)
                g.var_dict[variables[i]] = smt.smt_str_lit(text)
                g.var_assem_dict[variables[i]] = b
                g.var_num += 1
                add_var_flag(variables[i])
                assert (len(b) is not 0)

            if vars_num == 1:
                return variables[0]
            else:
                return variables
    else:
        if body is not None:
            litnodes.extend([make_random_literal(sort, body=i) for i in body])
        else:
            litnodes.extend([make_random_literal(sort) for _ in variables])
        g.var_dict.update(zip(variables, litnodes))
        for v in variables:
            add_var_flag(v)
        if vars_num == 1:
            return variables[0]
        else:
            return variables


def make_random_literal(sort, body=None):
    # if body is None:
    if sort == STRING_SORT:
        num = random.randint(1, g.max_lit_num)
        assem_var, new_text = make_assemble_Str(num)
        litnode = StringLitNode(new_text)
        return assem_var, litnode
    if sort == INT_SORT:
        if body is None:
            return IntLitNode(random.randint(g.min_int_lit, g.max_int_lit))
        else:
            return IntLitNode(body)

    if sort == BOOL_SORT:
        if body is None:
            return BoolLitNode(coin_toss())
        else:
            return BoolLitNode(body)
    raise ValueError('unknown sort {}'.format(sort))


def replace_termination():
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        vars = make_var_pairs(2, sort=STRING_SORT)
        lits = var_to_lits(vars[0])
        sub_lit = random_choose_lits(lits, 1)[0]
        sub_var = make_var_pairs(1, sort=STRING_SORT, body=[sub_lit])
        return smt.smt_replace(vars[0], sub_var, vars[1]), list_subtitude(lits, sub_var, var_to_lits(vars[1]))
    else:
        str_vars = get_str_vars()
        vars = random_choose_vars(str_vars, 2)
        target_lits = var_to_lits(vars[0])
        sub_lit = random_choose_lits(target_lits, 1)[0]
        if sub_lit in list(g.var_assem_dict.values()):
            sub_var = get_keys(g.var_assem_dict, sub_lit)
        else:
            sub_var = make_var_pairs(1, sort=STRING_SORT, body=[sub_lit])
        return smt.smt_replace(vars[0], sub_var, vars[1]), list_subtitude(target_lits, sub_lit, var_to_lits(vars[1]))


def substring_termination():
    all_vars = get_str_vars()
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        var = make_var_pairs(1, sort=STRING_SORT)
    else:
        var = random_choose_vars(all_vars)[0]
    # print('var:', var)
    lits = var_to_lits(var)
    # print('lits:', lits)
    sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
    match, index = list_match(lits, sub_lits)
    int_var1 = index[0]
    int_var2 = len(get_text(match))
    return smt.smt_substring(var, smt.smt_int_lit(int_var1), smt.smt_int_lit(int_var2)), match


def Lt_termination():
    if random.random() < g.new_variable_probability:
        int_vars = get_int_vars()
        if len(int_vars) > 2:
            paras = random_choose_vars(int_vars, 2)
            if g.var_dict[paras[0]].value < g.var_dict[paras[1]].value:
                return smt.smt_lt(paras[0], paras[1]), True
            else:
                return smt.smt_not(smt.smt_lt(paras[0], paras[1])), True
    variables = make_var_pairs(1, sort=INT_SORT)
    paras = random.randint(g.min_int_lit, g.max_int_lit)

    if g.var_dict[variables].value < paras:
        return smt.smt_lt(variables, smt.smt_int_lit(paras)), True
    else:
        return smt.smt_not(smt.smt_lt(variables, smt.smt_int_lit(paras))), True


def Lte_termination():
    if random.random() < 0.2:
        int_vars = get_int_vars()
        if len(int_vars) > 2:
            paras = random_choose_vars(int_vars, 2)
            # print(paras)
            para1 = g.var_dict[paras[0]].value
            para2 = g.var_dict[paras[1]].value
            if para1 <= para2:
                return smt.smt_lte(paras[0], paras[1]), True
            else:
                return smt.smt_not(smt.smt_lte(paras[0], paras[1])), True
    variables = make_var_pairs(1, sort=INT_SORT)
    paras = random.randint(g.min_int_lit, g.max_int_lit)
    if g.var_dict[variables].value <= paras:
        return smt.smt_lte(variables, smt.smt_int_lit(paras)), True
    else:
        return smt.smt_not(smt.smt_lte(variables, smt.smt_int_lit(paras))), True


def Gt_termination():
    if random.random() < 0.2:
        int_vars = get_int_vars()
        if len(int_vars) > 2:
            paras = random_choose_vars(int_vars, 2)
            paras1 = g.var_dict[paras[0]].value
            paras2 = g.var_dict[paras[1]].value
            if paras1 > paras2:
                return smt.smt_gt(paras[0], paras[1]), True
            else:
                return smt.smt_not(smt.smt_gt(paras[0], paras[1])), True
    variables = make_var_pairs(1, sort=INT_SORT)
    paras = random.randint(g.min_int_lit, g.max_int_lit)
    if g.var_dict[variables].value > paras:
        return smt.smt_gt(variables, smt.smt_int_lit(paras)), True
    else:
        return smt.smt_not(smt.smt_gt(variables, smt.smt_int_lit(paras))), True


def Gte_termination():
    if random.random() < 0.2:
        int_vars = get_int_vars()
        if len(int_vars) > 2:
            paras = random_choose_vars(int_vars, 2)
            paras1 = g.var_dict[paras[0]].value
            paras2 = g.var_dict[paras[1]].value
            if paras1 >= paras2:
                return smt.smt_gte(paras[0], paras[1]), True
            else:
                return smt.smt_not(smt.smt_gte(paras[0], paras[1])), True
    variables = make_var_pairs(1, sort=INT_SORT)
    paras = random.randint(g.min_int_lit, g.max_int_lit)
    if g.var_dict[variables].value >= paras:
        return smt.smt_gte(variables, smt.smt_int_lit(paras)), True
    else:
        return smt.smt_not(smt.smt_gte(variables, smt.smt_int_lit(paras))), True


def prefixof_termination():
    # print(len(g.var_assem_dict))
    # print((random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number)
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        variables = make_var_pairs(2, sort=STRING_SORT)
    else:
        variables = random_choose_vars(list(g.var_assem_dict.keys()), 2)
    lits = [var_to_lits(v) for v in variables]
    expression, models = prefixof_generator(variables, lits)
    return expression, models


def suffix_termination():
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        variables = make_var_pairs(2, sort=STRING_SORT)
    else:
        variables = random_choose_vars(list(g.var_assem_dict.keys()), 2)
    lits = [var_to_lits(v) for v in variables]
    # print(lits)
    expression, models = suffixof_generator(variables, lits)
    return expression, models


# def at_termination():
#     if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
#         var = make_var_pairs(1, sort=STRING_SORT)
#     else:
#         var = random_choose_vars(list(g.var_assem_dict.keys()))[0]
#         add_var_flag(var)
#
#     text = get_text(var)
#     int_var = random_int_variable(-1, len(text))
#     if int_var in range(len(text)):
#         target_char = text[int_var]
#         k = get_keys(g.assem_dict, target_char)
#         if len(k) is not 0:
#             return smt.AtNode(var, int_var), [k]
#         else:
#             new_lit = make_new_lit(target_char)
#             return smt.AtNode(var, int_var), [new_lit]
#     else:
#         return smt.AtNode(var, int_var), ['lit0']


def indexof2_termination():
    all_vars = get_str_vars()
    if len(all_vars) == 0:
        var = make_var_pairs(1, sort=STRING_SORT)
        if random.random() < 0.1:
            sub_var = make_var_pairs(1, sort=STRING_SORT)
        else:
            lits = var_to_lits(var)
            # print(lits)
            sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
            # print(sub_lits)
            sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
    elif (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        var = make_var_pairs(1, sort=STRING_SORT)
        if random.random() < 0.1:
            sub_var = random_choose_vars(all_vars)[0]
        else:
            # print('var:', var)
            lits = var_to_lits(var)
            sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
            sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
    else:
        if random.random() < 0.3:
            var = make_var_pairs(1, sort=STRING_SORT)
            # print('var:', var)
            lits = var_to_lits(var)
            # print('lits:', lits)
            sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
            # print(sub_lits)
            sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
        else:
            var = random_choose_vars(all_vars)[0]
            if random.random() < 0.5:
                sub_var = random_choose_vars(all_vars)[0]
            else:
                lits = var_to_lits(var)
                print(lits)
                sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
                print(sub_lits)
                sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
    all_int_vars = get_int_vars()
    var_match, ind = list_match(var, sub_var)
    text1 = get_text(var)
    text2 = get_text(sub_var)
    if len(all_int_vars) == 0:
        # print('ind1:', ind[0])
        int_var = make_var_pairs(1, sort=INT_SORT, body=ind[0])
        # print(g.var_dict[int_var].value)
    else:
        int_var = random_choose_vars(all_int_vars)[0]
    try:
        result = text1.index(text2, g.var_dict[int_var].value)
    except ValueError:
        result = -1
    return IndexOf2Node(var, sub_var, int_var), result


# def index_termination():
#     all_vars = get_str_vars()
#     if all_vars == 0:
#         var = make_var_pairs(1, sort=STRING_SORT)
#         if random.random() < 0.1:
#             sub_var = make_var_pairs(1, sort=STRING_SORT)
#         else:
#             lits = var_to_lits(var)
#             # print(lits)
#             sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
#             # print(sub_lits)
#             sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
#     elif (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
#         var = make_var_pairs(1, sort=STRING_SORT)
#         if random.random() < 0.1:
#             sub_var = random_choose_vars(all_vars)[0]
#         else:
#             lits = var_to_lits(var)
#             sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
#             sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
#     else:
#         if random.random() < 0.3:
#             var = make_var_pairs(1, sort=STRING_SORT)
#             lits = var_to_lits(var)
#             # print(lits)
#             sub_lits = random_choose_lits(lits, random.randint(1, len(lits)))
#             # print(sub_lits)
#             sub_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
#         else:
#             var = random_choose_vars(all_vars)[0]
#             sub_var = random_choose_vars(all_vars)[0]
#
#     text1 = get_text(var)
#     text2 = get_text(sub_var)
#     try:
#         result = text1.index(text2)
#     except ValueError:
#         result = -1
#     return IndexOfNode(var, sub_var), result
    # all_vars = get_str_vars()
    # if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
    #     var = make_var_pairs(1, sort=STRING_SORT)
    # else:
    #     weight = get_var_weight(all_vars)
    #     var = random.choices(all_vars, weights=weight, k=1)[0]
    # if len(all_vars) == 0:
    #     sub_var = make_var_pairs(1, sort=STRING_SORT)
    # else:
    #     weights = get_var_weight(all_vars)
    #     sub_var = random.choices(all_vars, weights=weights, k=1)[0]
    # text1 = get_text(var)
    # text2 = get_text(sub_var)
    # print(text1)
    # print(text2)
    # try:
    #     result = text1.index(text2)
    # except ValueError:
    #     result = -1
    # return IndexOfNode(var, sub_var), result


def contains_termination():
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        variable = make_var_pairs(1, sort=STRING_SORT)
        var_lits = var_to_lits(variable)
        sub_lits = random_choose_lits(var_lits, random.randint(1, len(var_lits)))
        new_var = make_var_pairs(1, sort=STRING_SORT, body=sub_lits)
        return smt.smt_contains(variable, new_var), True

    else:
        variables = random_choose_vars(list(g.var_assem_dict.keys()), 2)
        var_lits = [var_to_lits(v) for v in variables]
        return contains_generator(variables, var_lits)


def concat_termiatnion():
    all_vars = get_str_vars()
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        vars = make_var_pairs(2, sort=STRING_SORT)
    else:
        vars = random_choose_vars(all_vars, 2)
    lits0 = var_to_lits(vars[0])
    lits1 = var_to_lits(vars[1])
    # print(g.var_assem_dict)
    # print(type(lits0))
    # print(type(lits1))
    return smt.smt_concat(vars[0], vars[1]), lits0 + lits1


def Gt_generator(expression, int_var):
    if int_var[0] > int_var[1]:
        return smt.smt_gt(expression[0], expression[1]), True
    else:
        return smt.smt_not(smt.smt_gt(expression[0], expression[1])), True


def Gte_generator(expression, int_var):
    if int_var[0] >= int_var[1]:
        return smt.smt_gte(expression[0], expression[1]), True
    else:
        return smt.smt_not(smt.smt_gte(expression[0], expression[1])), True


def Lt_generator(expression, int_var):
    if int_var[0] < int_var[1]:
        return smt.smt_lt(expression[0], expression[1]), True
    else:
        return smt.smt_not(smt.smt_lt(expression[0], expression[1])), True


def Lte_generator(expression, int_var):
    if int_var[0] <= int_var[1]:
        return smt.smt_lte(expression[0], expression[1]), True
    else:
        return smt.smt_not(smt.smt_lte(expression[0], expression[1])), True


def contains_generator(expression, lits):
    text1 = literals_to_text(lits[0])
    text2 = literals_to_text(lits[1])
    if text1.find(text2) is not -1:
        return smt.smt_contains(expression[0], expression[1]), True
    elif text2.find(text1) is not -1:
        return smt.smt_contains(expression[1], expression[0]), True
    else:
        match_var, index_var = list_match(lits[0], lits[1])
        if len(match_var) == 0:
            return smt.smt_not(smt.smt_contains(expression[0], expression[1])), True
        match_text = get_text(match_var)
        if len(match_text) == 0:
            sub_lit = random_choose_lits(lits[0], random.randint(1, len(lits[0])))
            sub_expr = make_var_pairs(1, sort=STRING_SORT, body=sub_lit)
            return smt.smt_contains(expression[0], sub_expr), True
        if len(text1) > len(text2):
            return smt.smt_contains(expression[0],
                                    smt.smt_substring(expression[1],
                                                      smt.smt_int_lit(index_var[1]),
                                                      smt.smt_int_lit(len(match_text)))), True
        else:
            return smt.smt_contains(expression[0],
                                    smt.smt_substring(expression[1],
                                                      smt.smt_int_lit(index_var[1]),
                                                      smt.smt_int_lit(len(match_text)))), True

    # if father.value.find(son.value) is not -1:
    #     return ContainsNode(var1, var2), True
    # else:
    #     return ContainsNode(var1, var2), False
    # else:
    #     str_vars = get_str_vars()
    #     if len(str_vars) > 2:
    #         if random.random() < 0.3:
    #             for var1 in str_vars:
    #                 subvars = str_vars[:]
    #                 subvars.remove(var1)
    #                 for var2 in subvars:
    #                     match, index = list_match(var1, var2)
    #                     if len(match) is not 0:
    #                         text1 = get_text(var1)
    #                         text2 = get_text(var2)
    #                         text3 = get_text(match)
    #                         if text2 == text3:
    #                             return smt.smt_contains(var1, var2), True
    #                         elif text1 == text3:
    #                             return smt.smt_contains(var1, var2), True
    #                         else:
    #                             if random.random() < 0.5:
    #                                 return smt.smt_contains(var1, smt_substring(var2, IntLitNode(index[1]),
    #                                                                             IntLitNode(index[1] + len(text3))))
    #                             else:
    #                                 return smt.smt_contains(var2, smt_substring(var1, IntLitNode(index[0]),
    #                                                                             IntLitNode(index[0] + len(text3))))
    #         else:
    #             var1 = random.choice(str_vars)
    #             text = get_text(var1)
    #             min_str = random.randint(0, g.min_str_lit_length)
    #             max_str = random.randint(min_str, g.max_str_lit_length)
    #             sub_str = text[min_str:max_str]
    #             return smt.smt_contains(var1, StringLitNode(sub_str)), True


def At_generator(expressions, vars):
    text = get_text(vars[0])
    if len(text) <= vars[1] or vars[1] < 0:
        return AtNode(expressions[0], expressions[1]), ['lit0']
    else:
        text = get_text(vars[0])
        target_text = text[vars[1]]
        new_lit = make_new_lit(target_text)
        return AtNode(expressions[0], expressions[1]), [new_lit]


def replace_generator(expressions, lits):
    match01, index01 = list_match(lits[0], lits[1])
    match12, index12 = list_match(lits[1], lits[2])
    match02, index02 = list_match(lits[0], lits[2])
    if match01 == lits[1]:
        return StringReplaceNode(expressions[0], expressions[1], expressions[2]), replace_lit(lits[0], lits[1], lits[2],
                                                                                              index01[0])
    elif match01 == lits[0]:
        return StringReplaceNode(expressions[1], expressions[0], expressions[2]), replace_lit(lits[1], lits[0], lits[2],
                                                                                              index01[1])
    elif match12 == lits[2]:
        return StringReplaceNode(expressions[1], expressions[2], expressions[0]), replace_lit(lits[1], lits[2], lits[0],
                                                                                              index12[0])
    elif match12 == lits[1]:
        return StringReplaceNode(expressions[2], expressions[1], expressions[0]), replace_lit(lits[2], lits[1], lits[0],
                                                                                              index12[1])
    elif match02 == lits[2]:
        return StringReplaceNode(expressions[0], expressions[2], expressions[1]), replace_lit(lits[0], lits[2], lits[1],
                                                                                              index02[0])
    elif match02 == lits[0]:
        return StringReplaceNode(expressions[2], expressions[0], expressions[1]), replace_lit(lits[2], lits[0], lits[1],
                                                                                              index02[1])
    else:
        if random.random() < 0.1:
            target_expression = smt.smt_replace(expressions[0], expressions[1], expressions[2])
            return target_expression, ['lit0']
        if len(match01) is not 0:
            int_vars = make_var_pairs(2, sort=INT_SORT, body=[index01[1], index01[1] + len(match01)])
            target_expression = smt.smt_replace(expressions[0],
                                                smt.smt_substring(expressions[1], int_vars[0], int_vars[1]),
                                                expressions[2])
            return target_expression, replace_lit(lits[0], lits[1][index01[1]:index01[1] + len(match01)], lits[2],
                                                  index01[0])
        elif len(match12) is not 0:
            int_vars = make_var_pairs(2, sort=INT_SORT, body=[index12[1], index12[1] + len(match12)])
            target_expression = smt.smt_replace(expressions[1],
                                                smt.smt_substring(expressions[2], int_vars[0], int_vars[1]),
                                                expressions[0])
            return target_expression, replace_lit(lits[1], lits[2][index12[1]:index12[1] + len(match12)], lits[0],
                                                  index12[0])
        elif len(match02) is not 0:

            int_vars = make_var_pairs(2, sort=INT_SORT, body=[index02[1], index02[1] + len(match02)])
            target_expression = smt.smt_replace(expressions[1],
                                                smt.smt_substring(expressions[2], int_vars[0], int_vars[1]),
                                                expressions[0])
            return target_expression, replace_lit(lits[0], lits[2][index02[1]:index02[1] + len(match02)], lits[1],
                                                  index02[0])
        else:
            target_expression = smt.smt_replace(expressions[0], expressions[1], expressions[2])
            return target_expression, ['lit0']


def length_termination():
    all_vars = get_str_vars()
    if (random.random() < g.new_variable_probability or len(g.var_assem_dict) <= 2) and g.var_num < g.max_var_number:
        vars = make_var_pairs(1, sort=STRING_SORT)
    else:

        vars = random_choose_vars(all_vars)[0]
    return smt.smt_len(vars), len(get_text(vars))


def length_generator(expression, lits):
    # print(lits[0])
    text = get_text(lits[0])
    return smt.smt_len(expression[0]), len(text)


# def indexof_generator(expression, lits):
#     # print('indexof_generator:', lits[0])
#     text1 = get_text(lits[0])
#     text2 = get_text(lits[1])
#     # print('lits0:', lits[0])
#     # print('lits1:', lits[1])
#     if len(text1) < len(text2):
#         left = text2
#         right = text1
#         label = -1
#     else:
#         left = text1
#         right = text2
#         label = 1
#     try:
#         result = left.index(right)
#     except ValueError:
#         result = -1
#     if label == 1:
#         return IndexOfNode(expression[0], expression[1]), result
#     else:
#         return IndexOfNode(expression[1], expression[0]), result


def indexof2_generator(expression, lits):
    lits1 = lits[0]
    lits2 = lits[1]
    int_var = lits[2]
    text1 = get_text(lits1)
    text2 = get_text(lits2)
    if len(text1) < len(text2):
        left = text2
        right = text1
        label = -1
    else:
        left = text1
        right = text2
        label = 1
    try:
        result = left.index(right, int_var)
    except ValueError:
        result = -1
    if label == 1:
        return IndexOf2Node(expression[0], expression[1], expression[2]), result
    else:
        return IndexOf2Node(expression[1], expression[0], expression[2]), result


def prefixof_generator(expression, lits):
    text1 = get_text(lits[0])
    text2 = get_text(lits[1])
    if text1.startswith(text2):
        return smt.smt_prefixof(expression[0], expression[1]), True
    elif text2.startswith(text1):
        return smt.smt_prefixof(expression[1], expression[0]), True
    else:
        match, index = list_match(lits[0], lits[1])
        if len(match) is not 0:
            # int_vars1 = make_var_pairs(2, sort=INT_SORT, body=[index[0], len(text1) - index[0] - 1])
            # int_vars2 = make_var_pairs(2, sort=INT_SORT, body=[index[1], len(match)])
            return PrefixOfNode(
                smt.smt_substring(expression[0], smt.smt_int_lit(index[0]), smt.smt_int_lit(len(text1) - index[0])),
                smt.smt_substring(expression[1], smt.smt_int_lit(index[1]), smt.smt_int_lit(len(match)))), True
        else:
            return smt.smt_not(PrefixOfNode(expression[0], expression[1])), True


def suffixof_generator(expression, lits):
    # print(lits)
    text1 = get_text(lits[0])
    text2 = get_text(lits[1])
    if text1.endswith(text2):
        return smt.smt_prefixof(expression[0], expression[1]), True
    elif text2.endswith(text1):
        return smt.smt_prefixof(expression[1], expression[0]), True
    else:
        match, index = list_match(lits[0], lits[1])
        if len(match) is not 0:
            # int_vars1 = make_var_pairs(2, sort=INT_SORT, body=[0, index[0] + len(match)])
            # int_vars2 = make_var_pairs(2, sort=INT_SORT, body=[index[1], len(match)])
            int_vars1 = [IntLitNode(0), IntLitNode(index[0] + len(match))]
            int_vars2 = [IntLitNode(index[1]), IntLitNode(len(match))]
            return SuffixOfNode(smt.smt_substring(expression[0], int_vars1[0], int_vars1[1]),
                                smt.smt_substring(expression[1], int_vars2[0], int_vars2[1])), True
        else:
            return smt.smt_not(SuffixOfNode(expression[0], expression[1])), True


def substring_generator(expression, vars):
    lit = vars[0]
    int_var1 = vars[1]
    int_var2 = vars[2]
    position1 = check_lit_position(lit, int_var1)
    position2 = check_lit_position(lit, int_var2)
    # print('position1:', position1)
    # print('position2:', position2)
    # print('vars:', vars)
    if position1 == -2 or position2 == -2:
        return smt.smt_substring(expression[0], expression[1], expression[2]), ['lit0']
    elif position1 == -1 and position2 == -1:
        return smt.smt_substring(expression[0], expression[1], expression[2]), ['lit0']
    elif position1 == -1:
        gap2 = int_var2 - len(get_text(lit[:position2 + 1]))
        return smt.smt_substring(expression[0], IntMinusNode(expression[2], IntLitNode(gap2)), expression[1]), lit[
                                                         position2:]
    elif position2 == -1:
        gap1 = int_var1 - len(get_text(lit[:position1 + 1]))
        return smt.smt_substring(expression[0], IntMinusNode(expression[1], IntLitNode(gap1)), expression[2]), lit[
                                                                                                               position1:]
    else:
        if int_var1 < int_var2:
            gap1 = int_var1 - len(get_text(lit[:position1 + 1]))
            gap_lager2 = len(get_text(lit[:position2 + 1])) - int_var2
            return smt.smt_substring(expression[0], IntMinusNode(expression[1], IntLitNode(gap1)),
                                     IntPlusNode(expression[2], IntLitNode(gap_lager2))), lit[position1:position2 + 1]
        else:
            gap2 = int_var2 - len(get_text(lit[:position2 + 1]))
            gap_lager1 = len(get_text(lit[:position1 + 1])) - int_var1
            return smt.smt_substring(expression[0], IntMinusNode(expression[2], IntLitNode(gap2)),
                                     IntPlusNode(expression[1], IntLitNode(gap_lager1))), lit[position2:position1 + 1]


def concat_generator(expression, lits):
    lit1 = lits[0]
    lit2 = lits[1]
    return smt.smt_concat(expression[0], expression[1]), lit1 + lit2


def and_generator(expression, boolen_var):
    boolen1 = boolen_var[0]
    boolen2 = boolen_var[1]
    if boolen1 and boolen2:
        return smt.smt_and(expression[0], expression[1]), True
    else:
        return smt.smt_not(smt.smt_and(expression[0], expression[1])), True


def or_generator(expression, vars):
    boolen1 = vars[0]
    boolen2 = vars[1]
    if boolen1 or boolen2:
        return smt.smt_or(expression[0], expression[1]), True
    else:
        return smt.smt_not(smt.smt_or(expression[0], expression[1])), True


def find_eqaul(lits):
    candidate = {}
    cand_index = {}
    for var in list(g.var_assem_dict.keys()):
        matchVal, indexVal = list_match(lits, var)
        if len(matchVal) is not 0:
            candidate.update({var: matchVal})
            cand_index.update({var: indexVal})
    if len(candidate) == 0:
        return None, None, None
    else:
        target = random_choose_vars(list(candidate.keys()))[0]
    return target, candidate[target], cand_index[target]


def equal_generator(expression, vars):
    var1 = vars[0]
    var2 = vars[1]
    sort = expression[0].get_sort()
    if sort is INT_SORT or sort is BOOL_SORT:
        if var1 == var2:
            return smt.smt_equal(expression[0], expression[1]), True
        else:
            return smt.smt_not(smt.smt_equal(expression[0], expression[1])), True
    elif sort is STRING_SORT:
        test1 = get_text(var1)
        test2 = get_text(var2)
        if test1 == test2:
            return smt.smt_equal(expression[0], expression[1]), True
        else:

            match, ind = list_match(var1, var2)
            if len(match) == 0:
                new_var, match_var, new_index = find_eqaul(var1)
                if random.random() > 0.4 and new_var is not None:
                    match_lits = match_var
                    match_text = get_text(match_lits)
                    var_ind = new_index[0]
                    new_ind = new_index[1]
                    return smt.smt_equal(smt.smt_substring(expression[0], smt.smt_int_lit(var_ind),
                                                           smt.smt_int_lit(len(match_text))),
                                         smt.smt_substring(new_var, smt.smt_int_lit(new_ind),
                                                           smt.smt_int_lit(len(match_text)))), True
                else:
                    sub_lit = random_choose_lits(var1)
                    sub_text = get_text(sub_lit)
                    return smt.smt_equal(expression[0], smt.smt_str_lit(sub_text)), True
            else:
                match_lits = match
                match_text = get_text(match_lits)
                return smt.smt_equal(smt.smt_substring(expression[0], smt.smt_int_lit(ind[0]),
                                                       smt.smt_int_lit(len(match_text))),
                                     smt.smt_substring(expression[1], smt.smt_int_lit(ind[1]),
                                                       smt.smt_int_lit(len(match_text)))), True


    else:

        raise ValueError('unknown sort {}'.format(sort))

#
# if __name__ == "__main__":
#     expression, model = indexof2_termination()
#     print(expression)
#     print(model)
