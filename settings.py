import re

FuzzerPopulation 				        = 5
FuzzerNumberOfMutations		            = 2
FuzzerNumberOfHardestKept		        = 1
FuzzerNumberPopulationStart	            = 5
BugMode						            = False
GeneratorMaxDepth				        = 5
GeneratorNumConst				        = 5
NoBandit = False
num_assertions							= 5
timeout							        = 2500
theory = 'QF_SLIA'


InputFiles = []
mode = '' # cvc4, z3str3, z3seq, commit
solver_type = ''
solvers = []
commits = []
string_ops =  ['Concat', 'Contains', 'At', 'Length', 'IndexOf2', 'PrefixOf', 'SuffixOf', 'Replace', 'ReInter', 'ReRange', 'RePlus', 'ReStar', 'ReConcat', 'Str2Re', 'InRegex', 'ToInt', 'Substring']
file_name                               = ''
reg_num = 0
non_reg_num = 0
file_path = ''
non_reg_path = ''
diff_path = './diff'
file_num = 0
#outputdir
OutputDirectory = None
setInfo = re.compile(r'\(set-info .*\)')
reg_path = ''
init_time = 0
diff_num = 0

#about cases
MaxStr = 20
NumAssert = 15
max_var_num = 3
max_assert_num = 4
max_depth = 4
max_str_len = 20

MinStr = 10
MinAssert = 3
MinVar = 3
average_time = [0, 0]

### for Generators
new_var_probability = 0.0
found_time_list = [0, 0, 0]
op_dict = {}
all_run_time = []
all_time_diff = []