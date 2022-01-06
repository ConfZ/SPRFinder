import re
from enum import Enum, unique


@unique
class flag(Enum):
    good = 1
    bad = 2
    build_error = 3
    run_error = 4
    mid = 5
timeout = 20
current_cmt = ''
solver = 'seq'
cvc4_versions = {'cvc4-1.6': 'f8d6bd369',
                 'cvc4-1.7': '84da9c0b4',
                 'cvc4-1.8': '524790107',
                 'cvc4-1.9': '3a3735d58'}

z3_versions = {'z3-4.8.7': '30e7c225c',
               'z3-4.8.8': 'ad55a1f1c',
               'z3-4.8.9': '79734f26a'}
FIND_CMT = re.compile(r'.*\[(?P<COMMIT>\w*)\]')
FIND_TAR = re.compile(r'(?P<TAR>\w*) is the first bad commit')

# path = {'cvc4': '/home/zy/Documents/smt_editions/cvc4_editions/CVC4',
#         'z3str3': '/home/zy/Documents/smt_editions/z3_editions/z3',
#         'seq': '/home/zy/Documents/smt_editions/z3_editions/z3'}
case_path = ''
# cmd = {'cvc4': './cvc4 --strings-exp --tlimit=300000 ',
#        'z3seq': './z3 smt.string_solver=seq -T:300 ',
#        'z3str3': './z3 smt.string_solver=z3str3 -T:300 '}
root_path = ''
commits = []
commit_log= {}
cmt_case = {}
csv_path = ''
init_path = ''
have_found_dict = {}
unique_cmt = 0
father_path = ''
solvers = []

class parameters:
    def __init__(self):
        self.target_solver = ''
        self.root_path = ''
        self.case_path = ''
        self.father_path = ''
        self.solvers = []
        self.csv_path = ''
        self.init_path = ''
