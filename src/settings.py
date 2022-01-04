import re
FuzzerPopulation 				        = 5
FuzzerNumberOfMutations		            = 2
FuzzerNumberOfHardestKept		        = 1
FuzzerNumberPopulationStart	            = 5
BugMode						            = False
# GeneratorMaxDepth				        = 5
# GeneratorNumConst				        = 5
NoBandit = False
# num_assertions							= 5
timeout							        = 20
theory = 'QF_SLIA'
solvers = []

InputFiles = []
mode = '' # cvc4, z3str3, z3seq, commit


# commits = []
string_ops =  ['Concat', 'Contains', 'At', 'Length', 'IndexOf2', 'PrefixOf', 'SuffixOf', 'Replace', 'ReInter', 'ReRange', 'RePlus', 'ReStar', 'ReConcat', 'Str2Re', 'InRegex', 'ToInt', 'Substring']
file_name                               = ''
reg_num = 0
reg_path = ''
# non_reg_num = 0
file_path = ''
# non_reg_path = ''
# diff_path = './diff'
# file_num = 0
#outputdir
OutputDirectory = None
setInfo = re.compile(r'\(set-info .*\)')
init_time = 0
diff_num = 0
#pre-defined parameter
max_var_num = 3
max_assert_num = 4
max_depth = 4
max_str_len = 20

average_time = [0, 0]

#about cases
NumAssert = 15


# Maximum Parameter
MaxStr = 500
MaxVarNum = 20
MaxAssertNum = 15
MaxDepth = 6

# Minimum Parameter
MinStr = 10
MinVarNum = 3
MinAssertNum = 3
MinDepth = 2


### for Generators
it = 0
new_var_probability = 0.0
found_time_list = [0, 0, 0]
op_dict = {}
all_run_time = []
all_time_diff = []

class para:
    def __init__(self):
        self.type = ''
        self.timeout = 20
        self.root_path = ''
        self.max_var_num = 3
        self.max_assert_num = 4
        self.max_depth = 4
        self.max_str_len = 20
        self.time0 = 0


