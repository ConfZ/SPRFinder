import SMT_generator.smt as smt
import SMT_generator.ast as sast
import string
import random
import SMT_generator.generator as generator
from SMT_generator.constants import SMT_25_STRING
import timeout_decorator
import time
import os
import pandas as pd

# import SMT_generator.generators.concats as concat
# import SMT_generator.generators.concats as concat

# ALPHABET = string.digits + string.ascii_letters + string.punctuation
ALPHABET = string.digits + string.ascii_letters
# WHITESPACE = string.whitespace
# ALL_CHARS = ALPHABET + WHITESPACE
ALL_CHARS = ALPHABET
SYNTACTIC_DEPTH = 'syntactic'
SEMANTIC_DEPTH = 'semantic'
var_num = 0
var_dict = {}

SUFFIXOF = 'suffixof'
PREFIXOF = 'prefixof'
CONTAINS = 'contains'

def set_equal(a, b):
    return smt.smt_assert(smt.smt_equal(a, b))


def smt_replace(a, b, c):
    return sast.StringReplaceNode(a, b, c)


def set_concat(result, a, b):
    return set_equal(result, smt.smt_concat(a, b))


def set_replace(result, a, b, c):
    return set_equal(result, smt_replace(a, b, c))


def random_text(length):
    return ''.join(random.choice(ALL_CHARS) for _ in range(0, length))

def random_bool():
    return random.choice([True, False])

def smt_suffixof(a, b):
    return sast.SuffixOfNode(b, a)
def smt_prefixof(a, b):
    return sast.PrefixOfNode(b, a)
def smt_contains(a, b):
    return sast.ContainsNode(a, b)
def get_key(dic):
    key = list(dic.keys())
    return key[0]

def random_suffixof():
    global var_dict
    base_var = random.choice(list(var_dict.keys()))
    type = random.randint(0,1)
    base_model = var_dict[base_var].value
    if len(base_model) is 0:
        return None
    sub_str = base_model[random.randint(0, len(base_model))-1: -1]
    if type == 0:
        return smt.smt_assert(smt_suffixof(base_var, sast.StringLitNode(sub_str)))
    else:
        new_str = make_var_pair(1, sort = smt.STRING_SORT, body=[sub_str])
        return smt.smt_assert(smt_suffixof(base_var, get_key(new_str)))
def random_substr(str):
    # print('strlen:'+ str)
    index = random.randint(0, len(str)-1)
    index2 = random.randint(index, len(str))
    return str[index:index2]
def random_prefixof():
    global var_dict
    base_var = random.choice(list(var_dict.keys()))
    type = random.randint(0, 1)
    base_model = var_dict[base_var].value
    if len(base_model) is 0:
        return None
    # print('base_model:'+base_model)
    sub_str = base_model[0: random.randint(1, len(base_model))]
    if type == 0:
        return smt.smt_assert(smt_prefixof(base_var, sast.StringLitNode(sub_str)))
    else:
        new_str = make_var_pair(1, sort = smt.STRING_SORT, body=[sub_str])
        # print(new_str)
        return smt.smt_assert(smt_prefixof(base_var, get_key(new_str)))
def random_contains():
    global var_dict
    base_var = random.choice(list(var_dict.keys()))
    type = random.randint(0, 1)
    base_model = var_dict[base_var].value
    if len(base_model) is 0:
        return None
    # print(var_dict)
    # print('base_model:'+ base_model)
    sub_str = random_substr(base_model)
    if type == 0:
        return smt.smt_assert(smt_contains(base_var, sast.StringLitNode(sub_str)))
    else:
        new_str = make_var_pair(1, sort=smt.STRING_SORT, body=[sub_str])
        # print(new_str)
        return smt.smt_assert(smt_contains(base_var, get_key(new_str)))

def random_equal():
    s = random.choice(list(var_dict.keys()))
    return set_equal(s, var_dict[s])


SOLUTION_GENERATORS = [
    random_suffixof,
    random_prefixof,
    random_contains,
]
def make_random_lit(sort, length=100, body=None):
    if body is None:
        if sort == sast.STRING_SORT:
            return sast.StringLitNode(random_text(length))
        if sort == sast.INT_SORT:
            return sast.IntLitNode(random.randint(0, length))

        if sort == sast.BOOL_SORT:
            return sast.BoolLitNode(random_bool())
    else:
        if sort == sast.STRING_SORT:
            return sast.StringLitNode(body)
        if sort == sast.INT_SORT:
            return sast.IntLitNode(body)

        if sort == sast.BOOL_SORT:
            return sast.BoolLitNode(body)


def make_var_pair(var_n, sort, body=None, max=100, min=1):
    varibles = [smt.smt_new_var() for _ in range(var_n)]
    # print(varibles)
    if body is not None:
        text = [make_random_lit(sort, body=i) for i in body]
    else:
        text_len = [random.randint(min, max) for _ in range(var_n)]
        text = [make_random_lit(sort, length=i) for i in text_len]
    global var_dict

    result = dict(zip(varibles, text))
    var_dict.update(result)
    # print(result)

    return result


def make_single_pair(var, sort, body=None, max=100, min=0):
    varible = smt.smt_var(var)
    text_len = range(min, max)
    text = make_random_lit(sort, text_len)
    global var_dict
    var_dict.update(zip(varible, text))
    return dict(zip(varible, text))


def make_sematic_concats(depth=10, balanced=False):
    global var_num, var_dict
    if balanced is True:
        raise ValueError('balanced trees with semantic concats are unsupported')
    # base_value = {key: value for key, value in var_dict if key < 0}
    num = (depth * 2) + 1
    var_num += num
    # values = []
    # for v in base_value.values():
    #     values.append(v.value)
    # var3 = make_var_pair(1, sast.STRING_SORT, body=values[0].value+values[1].value)
    var1 = make_var_pair(1, sort=sast.STRING_SORT)
    var2 = make_var_pair(1, sort=sast.STRING_SORT)
    varibles = []
    varibles.append(list(var1.keys())[0])
    varibles.append(list(var2.keys())[0])
    expressions = []
    for i in range(0, num - 2, 2):
        vars = list(varibles())
        var_left = vars[-2]
        var_right = vars[-1]
        var_new = make_var_pair(1, sast.STRING_SORT, body=[varibles[var_left].value + varibles[var_right].value])
        var_new = list(var_new.keys())[0]

        expression = set_concat(var_new, var_left, var_right)
        varibles.append(var_new)
        expressions.append(expression)
    return varibles, expressions


def make_syntactic_concats(depth, balanced):
    make_var_pair(var_n=2, sort=sast.STRING_SORT)
    global var_num, var_dict

    def helper(depth, balanced):
        if depth < 1:
            new_var = make_var_pair(var_n=1, sort=sast.STRING_SORT)
            var_v = list(new_var.keys())[0]
            return [var_v], var_v
        right_vars, right_expr = helper(depth - 1, balanced)

        if balanced is True:
            left_vars, left_expr = helper(depth - 1, balanced)
        else:
            left_vars, left_expr = helper(0, balanced)

        all_vars = left_vars + right_vars
        expr = smt.smt_concat(left_expr, right_expr)
        return all_vars, expr

    def model_helper(concat):
        if isinstance(concat, sast.IdentifierNode):
            con_model = var_dict[concat].value
            return con_model

        elif isinstance(concat, sast.ConcatNode):
                string_left = model_helper(concat.body[0])
                string_right = model_helper(concat.body[1])
                con_model = string_left + string_right
                return con_model
        else:
            return "a"

    first_var = smt.smt_new_var()
    variables = [first_var]
    expression = []
    if depth > 0:
        concat_variables, concat_expr = helper(depth, balanced)
        # print(concat_variables)
        variables += concat_variables
        first_var_model = model_helper(concat_expr)
        first_var_model = sast.StringLitNode(first_var_model)
        # print(type(first_var))
        # print(type(list(var_dict.keys())[0]))
        var_dict[first_var] = first_var_model
        expression = [set_equal(first_var, concat_expr)]

    return variables, expression


def generate_concat(**kwargs):
    # create str variables
    global var_num
    if 'var_num' in kwargs.keys():
        var_num = kwargs['var_num']
    else:
        var_num = random.randint(10, 100)
    if 'depth_type' in kwargs.keys():
        depth_type = kwargs['depth_type']
    else:
        depth_type = SYNTACTIC_DEPTH
    if 'depth' in kwargs.keys():
        depth = kwargs['depth']
    else:
        depth = random.randint(2, 10)
    if 'balanced' in kwargs.keys():
        balanced = kwargs['balanced']
    else:
        balanced = random_bool()
    if depth_type == SEMANTIC_DEPTH:
        variables, expressions = make_sematic_concats(depth, balanced)
    else:
        variables, expressions = make_syntactic_concats(depth, balanced)

    return variables, expressions


def random_choose(values, num):
    var_set = set()
    for _ in range(num):
        s = random.choice(values)
        var_set.add(s)
    return list(var_set)


def max_text_var(args):
    max_var = args[0]
    for n in args:
        if len(var_dict[max_var].value) < len(var_dict[n].value):
            max_var = n
    return max_var


def min_text_var(args):
    min_var = args[0]
    for n in args:
        if len(var_dict[min_var].value) > len(var_dict[n].value):
            min_var = n
    return min_var


def init_generate():
    global var_num, var_dict
    smt.smt_init()
    var_num = 0
    var_dict = {}


def get_definitions():
    global var_dict
    definitions = []
    for v in var_dict.keys():
        if isinstance(var_dict[v], sast.StringLitNode):
            definitions.append(smt.smt_declare_var(v, sort='String'))
        if isinstance(var_dict[v], sast.IntLitNode):
            definitions.append(smt.smt_declare_var(v, sort='Int'))
        if isinstance(var_dict[v], sast.BoolLitNode):
            definitions.append(smt.smt_declare_var(v, sort='Bool'))
    return definitions

def make_len(str_var, int_var):
    return set_equal(smt.smt_len(str_var), sast.IntLitNode(int_var))


def generate_solutions(**kwargs):
    generated = []
    if 'solution' in kwargs.keys():
        solution_num = kwargs['solution']
        for _ in range(solution_num):
            operator = random.choice(SOLUTION_GENERATORS)
            op = operator()
            if op is not None:
                generated.append(op)
            else:
                continue

    else:
        for _ in range(random.randint(1, 3)):
            operator = random.choice(SOLUTION_GENERATORS)
            op = operator()
            if op is not None:
                generated.append(op)
            else:
                continue

    return generated


def save_model(path):
    df = pd.DataFrame()

def generate(**kwargs):
    # check args
    init_generate()
    # print(var_dict)
    global var_dict
    variables, expressions = generate_concat(**kwargs)
    # print(variables)

    if 'length' in kwargs.keys():
        length_num = kwargs['length']
        len_var = set()
        for _ in range(length_num):
            s = random.choice(variables)
            len_var.add(s)
        len_var = list(len_var)
        for v in len_var:
            expressions.append(make_len(v, len(var_dict[v].value)))
    elif random.random() <= 0.1:
        length_num = random.randint(1, len(variables))
        len_var = set()
        for _ in range(length_num):
            s = random.choice(variables)
            len_var.add(s)
        len_var = list(len_var)
        for v in len_var:
            expressions.append(make_len(v, len(var_dict[v].value)))
    # print(expressions)
    if 'replace' in kwargs.keys():
        replace_num = kwargs['replace']
        assert replace_num < len(variables), "too many replace operations"
        var_num = random.randint(1, 2)
        for _ in range(replace_num):
            replace_var = random_choose(variables, var_num)
            if len(replace_var) == 1:
                base_var = replace_var[0]
                # while type()
                base_model = var_dict[base_var].value
                # base_len = len(base_model)
                end = random.randint(1, len(base_model))
                # print(type(end))
                subStr = base_model[0: end]
                randStr = random_text(random.randint(1, 10))
                new_model = base_model.replace(subStr, randStr, 1)
                new_var = make_var_pair(1, sort=sast.STRING_SORT, body=[new_model])
                # print(new_var)
                variables.append(list(new_var.keys())[0])
                expressions.append(
                    set_replace(list(new_var.keys())[0], base_var, smt.smt_str_lit(subStr), smt.smt_str_lit(randStr)))
            elif len(replace_var) == 2:
                position_value = random.randint(1, 2)
                base_var = max_text_var(replace_var)
                base_model = var_dict[base_var].value
                replace_var.remove(base_var)
                sub_var = random.choice(replace_var)
                sub_mode = var_dict[sub_var].value

                end = random.randint(1, len(base_model))

                if position_value == 1:
                    subStr = base_model[0: end]
                    new_model = base_model.replace(subStr, sub_mode, 1)
                    new_var = make_var_pair(1, sast.STRING_SORT, body=[new_model])
                    expressions.append(set_replace(list(new_var.keys())[0], base_var, smt.smt_str_lit(subStr),
                                                   sub_var))
                    variables.append(list(new_var.keys())[0])
                elif position_value == 2:
                    subStr = random_text(100)
                    new_model = base_model.replace(sub_mode, subStr, 1)
                    new_var = make_var_pair(1, sast.STRING_SORT, body=[new_model])
                    expressions.append(set_replace(list(new_var.keys())[0], base_var, sub_var,
                                                   smt.smt_str_lit(subStr)))
                    variables.append(list(new_var.keys())[0])

        solutions = generate_solutions(**kwargs)
        expressions.extend(solutions)
        definitions = get_definitions()
        # print(variables)
        definitions = [smt.smt_string_logic()] + definitions
        # definitions.extend([smt.smt_declare_var(v) for v in variables])
        # # print(definitions)
        # definitions.extend([smt.smt_declare_var(v, sort=sast.INT_SORT) for v in variables])
        # if int_variables is not False:
        #     definitions.extend([smt.smt_declare_var(v, sort=sast.INT_SORT) for v in int_variables])
        expressions.append(smt.smt_check_sat())
        # print(var_dict.keys())
        return definitions + expressions
@timeout_decorator.timeout(120)
def getCmd(cmd):
    print(cmd)
    start = time.time()
    result = os.popen(cmd, "r")
    text = result.read()
    result.close()
    end = time.time()
    delay = end - start
    return text, delay

if __name__ == '__main__':
    i = 1
    NAME = []
    RESULT = []
    TIME = []
    while i < 1000:
        file_name = 'test'+str(i)
        NAME.append(file_name)
        generated = generate(
            length=2,
            replace=2,
            solution=3,
            depth = 2,
        )
        # text = generator.generate(generated, SMT_25_STRING)
        name = r'/home/zy/Desktop/test_result/generate_sat/'+file_name+'.smt2'
        generator.generate_file(generated, SMT_25_STRING, name)
        # z3cmd = "z3 smt.string_solver=z3str3" + name
        # try:
        #     z3text, z3delay = getCmd(z3cmd)
        # except Exception:
        #     z3text = 'Timeout'
        #     z3delay = 900
        #
        #     # each.append("None")
        # z3_result = ' '
        # if re.match(".*unsat.*", z3text):
        #     z3_result = 'unsat'
        # elif re.match(".*sat.*", z3text):
        #     z3_result = 'sat'
        # if len(z3_result) == 0:
        #     z3_result = 'unknown'
        # RESULT.append(z3_result)
        # if z3_result == 'unsat':
        #     generator.generate_file(generated, SMT_25_STRING, '/home/zy/Desktop/test_result/bugs'+ file_name + '.smt2')
        # if z3delay > 120:
        #     generator.generate_file('//home/zy/Desktop/test_result/slower' + file_name + '.smt2')
        i += 1
    # data = {'name': NAME,
    #         'time': TIME,
    #         'result': RESULT}
    # df = pd.DataFrame(data, columns=['name', 'time', 'result'])
    # df.to_csv("/home/zy/Desktop/test_result_z3/z3Test.csv", encoding="utf-8-sig", mode="a", header=False, index=False)

