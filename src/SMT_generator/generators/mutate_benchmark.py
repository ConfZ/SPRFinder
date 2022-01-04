from SMT_generator.constants import SMT_20, SMT_20_STRING, SMT_25_STRING
from SMT_generator.scanner import scan, ALPHABET, WHITESPACE
from SMT_generator.parser import parse_file
import re
from SMT_generator.generator import generate
from SMT_generator.smt import *
from z3.z3 import parse_smt2_string
import SMT_generator.ast as sast
import z3
import SMT_generator.generator as generator
# set global config
_max_terms = 0
_max_str_lit_length = 0
_max_int_length = 0
_lit_probability = 0
_language = SMT_25_STRING
# patterns
CONCATS = 'concats'
LENGTHS = 'length'
REP_LEN_ = 'replace_concats'

EXP_TYPE_RE = re.compile(r"\('Id<(?P<EXPTYPE>[\w-]*)>'\s+.*\)")


def getExType(expression):
    global EXP_TYPE_RE
    expresionType = re.match(EXP_TYPE_RE, str(expression)).group('EXPTYPE')
    return expresionType


def expr_node(filepath, language=SMT_25_STRING):
    return parse_file(filepath, language)


def split2pool(expressions):
    exprPool = []
    stack = []
    for expr in expressions:
        if isinstance(expr, sast.AssertNode):
            stack.append(expr.body[0])
    while stack:
        item = stack[-1]
        stack.pop()
        if isinstance(item, sast.AndNode) or isinstance(item, sast.OrNode) or isinstance(item, sast.NotNode) or isinstance(item, sast.IteNode):
            subNode = item.body
            for nd in subNode:
                stack.append(nd)
        else:
            exprPool.append(item)
    return exprPool

# def model2expr(medol, expr):
#
def getModel(*args, **keywords):
    s = z3.Solver()
    s.set(**keywords)
    # print(*args)
    s.add(*args)
    r = s.check()
    if r == z3.unsat:
        return None
    elif r == z3.unknown:
        print('unknown SMT file')
        try:
            result = s.model()
            return result
        except z3.Z3Exception:
            return None
    else:
        result = s.model()
        return result


def modelExpression(model):
    dec = model.decls()
    vars = [str(v) for v in model.decls()]
    # print(vars)
    ref = [repr(model[r]) for r in dec]
    print(ref)

    return dict(zip(vars, ref))


def remove_slash(val):
    if repr(val).find('\\') is not -1:
        str = eval(repr(val).replace('\\', '\\\\'))
    else:
        str = val
    return str


# formula is generated from seed.
# sub is the new generated sub formula
def checkFormula(model, sub, z=None):
    values = modelExpression(model)
    new_expression = []
    new_expression.append(smt_string_logic())
    for k in values.keys():
        val = str(values[k])
        if val.isdigit() is True:
            new_expression.append(smt_declare_var(k, sort=sast.INT_SORT))
        else:
            new_expression.append(smt_declare_var(k, sort=sast.STRING_SORT))
    for v in values.keys():
        new_expression.append(smt_assert(smt_equal(v, remove_slash(values[v]))))
    new_expression.append(sub)
    new_expression.append(smt_check_sat())

    generated = generate(new_expression, _language)
    # print(generated)

    pss = parse_smt2_string(generated, sorts={}, decls={})
    print(pss)
    s = z3.Solver()
    s.add(pss)
    r = s.check()
    if r is z3.sat:
        return True
    else:
        return False
# def genenrate_concats():

# def generateNode(path, depth):


# def make_concate(depth, depth_type, ):
if __name__ == "__main__":
    # expresionNode = expr_node('/home/zy/Documents/stringfuzz_revised/demos/ex9.smt2')
    # print(expresionNode)
    # generator.generate_file(expresionNode, SMT_25_STRING, r'/home/zy/Documents/generate_sat/' + 'test0' + '.smt2')
    print(len("'\x0c'1/d'\n'Z1"))
    # # pool = split2pool(expresionNode)
    # #
    # # print(pool)
    # print(expresionNode)
    # expresion = generate(expresionNode, SMT_25_STRING)
    # # print(expresion)
    # constrain = parse_smt2_string(expresion, sorts={}, decls={})
    # ss = parse_smt2_string(expresion, sorts={}, decls={})
    # # print(constrain)
    # mod = getModel(constrain)
    # print(mod)
    # # print(expresionNode[3])
    # bb = checkFormula(mod, expresionNode[6])
    # #
    # # print(bb)
    # # ss = sc.scan_file('/home/zy/Documents/stringfuzz_revised/demos/ex9.smt2', SMT_25_STRING)
    # # print(ss)