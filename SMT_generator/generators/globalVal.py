import string
from SMT_generator.ast import *
#about variables:
is_shark = 'Off'
max_var_number = 20
var_num = 0
var_called_times = 0
new_variable_probability = 0.7

#about literals:
max_lit_length = 500
min_lit_length = 10
max_lit_num = 4
max_int_lit = 500
min_int_lit = 0
min_str_lit_length = 1
lit_called_times = 0
max_depth = 20

literal_probability = 0.2
ALPHABET = string.digits + string.ascii_letters  # + string.punctuation
sub_str_counter = 0
var_dict = {}


assem_dict = {}
flag_dict = {}
var_assem_dict = {}
var_flag_dict = {}
EXPRESSION_SORTS = DECLARABLE_SORTS  # + [REGEX_SORT]
