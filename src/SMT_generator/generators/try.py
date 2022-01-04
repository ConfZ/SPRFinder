from SMT_generator.generators.random_ast_zy import make_random_ast
from SMT_generator.generator import generate
if __name__ == '__main__':
    ast, res = make_random_ast(max_var_num = 20, max_terms = 20, max_depth=4, max_str_lit_length=100, max_int_lit=100, literal_probability=0.1, new_var_probability=0.5,
                    semantically_valid=False)
    print(generate(ast))