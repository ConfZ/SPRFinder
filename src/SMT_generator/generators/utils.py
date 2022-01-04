from SMT_generator.ast import *
import random
import bin.globalVal as g


def add_flag(substr):
    g.lit_called_times += 1
    if substr not in list(g.flag_dict.keys()):
        g.flag_dict[substr] = 1
    flag_d = g.flag_dict[substr]
    flag_d = flag_d + 1
    g.flag_dict[substr] = flag_d


def add_var_flag(var):
    g.var_called_times += 1
    if var not in list(g.var_flag_dict.keys()):
        g.var_flag_dict[var] = 1
    else:
        flag_d = g.var_flag_dict[var]
        flag_d = flag_d + 1
        g.var_flag_dict[var] = flag_d


def get_flag(substr):
    return g.flag_dict[substr]


def get_var_flag(var):
    print('var_flag_dict:', g.var_flag_dict)
    print('var_dict:', g.var_dict.keys())
    return g.var_flag_dict[var]


def get_int_vars():
    int_vars = list(filter(lambda key: isinstance(g.var_dict[key], IntLitNode), list(g.var_dict.keys())))
    return int_vars


def get_str_vars():
    str_vars = list(filter(lambda key: isinstance(g.var_dict[key], StringLitNode), list(g.var_dict.keys())))
    return str_vars


def get_bool_vars():
    bool_vars = list(filter(lambda key: isinstance(g.var_dict[key], BoolLitNode), list(g.var_dict.keys())))
    return bool_vars


def _get_weight(v, max_num, shark = 'Off'):
    if isinstance(v, IdentifierNode):
        weight_value = get_var_flag(v)

    elif v in list(g.assem_dict.keys()):

        weight_value = get_flag(v)
    else:
        raise ValueError('unknown sort {}'.format(type(v)))
    if shark == 'Off':
        w = max_num - weight_value
    else:
        w = weight_value
    if w < 1:
        w = 1
    return w

def get_var_weight(vars=None):
    if vars is None:
        target = list(g.var_flag_dict.keys())
    else:
        target = vars
    weights = [_get_weight(v, g.var_called_times, 'On') for v in target]
    return weights


def replace_lit(lit1, lit2, lit3, index):
    tmp1 = lit1[0:index]
    tmp2 = lit1[index + len(lit2):]
    new_lit = tmp1 + lit3 + tmp2
    return new_lit


def get_lit_weights(lits):
    weights = [_get_weight(v, g.lit_called_times, g.is_shark) for v in list(lits)]
    return weights


def var_to_lits(var):
    lit_vars = g.var_assem_dict[var]
    # lits = [g.assem_dict[l] for l in lit_vars]
    return lit_vars


def literals_to_text(lits):
    text = ''
    print('literal_to_text:', lits)
    for lit in lits:
        text += g.assem_dict[lit]
    return text


def is_in(list1, list2):
    for li in list1:
        if li not in list2:
            return False
    return True

def get_text(var):
    print('var:', var)
    print('var_assem_dict:', g.var_assem_dict)
    print('assem_dict', g.assem_dict)
    if var in list(g.var_assem_dict.keys()):
        lits = var_to_lits(var)
        # print(lits)
        text = literals_to_text(lits)
        print('branch1')
        return text
    elif var in list(g.assem_dict.keys()) and not isinstance(var, list):
        text = g.assem_dict[var]
        print('branch2')
        return text
    elif is_in(var, list(g.assem_dict.keys())) and isinstance(var, list):
        text = literals_to_text(var)
        print('branch3')
        return text
    else:
        print('branch4')
        raise ValueError('unknown sort {}'.format(var))



def list_match(var1, var2):
    if isinstance(var1, IdentifierNode):
        list1 = g.var_assem_dict[var1]
    else:
        list1 = var1
    if isinstance(var2, IdentifierNode):
        list2 = g.var_assem_dict[var2]
    else:
        list2 = var2
    i = 0
    list3 = []
    index = []
    while i < len(list1):
        j = 0
        p = i
        while j < len(list2) and p < len(list1):
            tmp = []
            ind = []
            if list1[p] == list2[j]:
                ind = [p, j]
            while list1[p] == list2[j]:
                tmp.append(list1[p])
                p += 1
                j += 1
                if p >= len(list1) or j >= len(list2):
                    break
            if len(list3) < len(tmp):
                list3 = tmp
                index = ind
            j += 1
        i += 1
        # print(list1, list2)
        # print(list3)
    if len(list3) == 0:
        return list3, [0, 0]
    else:
        return list3, [litindex_to_textIndex(list1, index[0]), litindex_to_textIndex(list2, index[1])]


def litindex_to_textIndex(lits, index):
    if index <= 0:
        return 0
    else:
        text = get_text(lits[:index])
        # print(lits[:index])
        # print(text)
        return len(text) - 1


def get_keys(dict, value):
    return [k for k, v in dict.items() if v == value]


def check_lit_position(lit, int_var):
    lit_len = [len(get_text(v)) for v in lit]
    length = 0
    if int_var < 0:
        return -2
    for i in range(len(lit_len)):
        length += lit_len[i]
        if length > int_var:
            return i
    return -1


def list_subtitude(list1, sub, list2):
    target = -1
    if isinstance(sub, list):
        item = sub[0]
    else:
        item = sub
    for i in range(len(list1)):
        if list1[i] == item:
            target = i
            break
    if target == -1:
        return list1
    else:
        left = list1[:target]
        right = list1[target + 1:]
        result = left + list2 + right
        return result


def random_choose_vars(vars, num=1):
    print('vars:', vars)
    weights = get_var_weight(vars)
    print('weight:', weights)
    target = random.choices(vars, weights, k=num)
    for var in target:
        add_var_flag(var)
    return target


def random_choose_lits(lits, num=1):
    # print('lits:', lits)
    weights = get_lit_weights(lits)
    # print('weight:', weights)
    target = random.choices(lits, weights=weights, k=num)
    for lit in lits:
        add_flag(lit)
    return target


if __name__ == '__main__':
    g.assem_dict = {'lit1': 'fasffghvz',
                    'lit2': "fbjmhh",
                    'lit3': 'bnfhgaa'}
    var111 = ['lit1', 'lit2', 'lit3']
    var33 = 'lit2'
    var222 = ['lit4', 'lit2', 'lit3', 'lit5']
    print(get_text(['lit1', 'lit2', 'lit3']))
