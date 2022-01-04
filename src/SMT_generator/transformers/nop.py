from SMT_generator.parser import parse

__all__ = [
    'nop',
]

# public API
def nop(ast):
    return ast
