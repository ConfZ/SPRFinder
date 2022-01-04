import os
import sys
from pathlib import Path
# import src.settings as settings
path = Path(__file__)
root_path = path.parent.absolute().parent
sys.path.append(str(root_path))
sys.path.append(str(root_path / 'src'))
print(root_path)

from src.settings import para
import src.fuzzer as fuzzer
import pandas as pd
import time
from src.parser import args


def delete_cases(path):
    if os.path.exists(path):
        for fpath, _, file_list in os.walk(path):
            for fname in file_list:
                if fname.endswith('.smt2'):
                    os.remove(os.path.join(fpath, fname))
        print('have deleted ', path)

def main():
    # settings.timeout = args.timeout
    #
    # # Maximum Parameter
    # settings.MaxDepth =  6
    # settings.MaxVarNum =   20
    # settings.MaxAssertNum = 15
    # settings.MaxStr = 500
    #
    # # Minimum Parameter
    # settings.MinStr = 10
    # settings.MinAssert = 3
    # settings.MinVar = 3
    # settings.MinDeep = 2
    #
    #
    # para.max_var_num = 3
    # para.max_assert_num = 4
    # para.max_depth = 4
    # para.max_str_len = 20


    # father = root_path.cwd()
    #
    # settings.string_ops = [
    #     # 'and','or','not','=','
    #     'Concat', 'Contains', 'Length', 'IndexOf', 'IndexOf2', 'PrefixOf', 'SuffixOf', 'Replace', 'Substring',
    #     'FromInt', 'ToInt',
    #     # 'InRegex','At',
    #     'Str2Re', 'ReConcat', 'ReStar', 'RePlus', 'ReRange', 'ReUnion', 'ReInter'
    # ]
    parameter = para()

    parameter.type = args.type
    # settings.solver_type = settings.mode
    #
    # settings.file_name = settings.mode
    parameter.solvers = args.solvers
    parameter.root_path = root_path
    parameter.timeout = args.timeout
    # if args.type == 'cvc4':
    #     settings.theory = 'QF_SLIA'
    # elif args.type == 'z3str3' or settings.mode == 'z3seq':
    #     settings.theory = 'QF_S'
    # # elif settings.mode == 'commit':
    # #     solvers = settings.commits
    # else:
    #     assert False, 'wrong mode'
    # for solver in solvers:
    #     assert os.path.isfile(solver), "No path to: " + solver
    # settings.solvers = list(solvers)

    # settings.reg_path = root_path / 'results'
    parameter.time0 = time.time()
    delete_cases(str(parameter.root_path/'results'/'Regression_cases'))
    finder = fuzzer.Fuzzer(parameter)
    # finder.init_set(parameter)
    finder.run()

if __name__ == '__main__':

    print(os.getcwd())
    df = pd.DataFrame(columns=['time', 'case_number'])
    df.to_csv('./results/Statistics/Total_number.csv')
    df1 = pd.DataFrame(columns=['case', 'solver1', 'solver2', 'solver3', 'var_num', 'assert_num', 'nax_str_len', 'max_depth'])
    df1.to_csv('./results/Statistics/Results_for_cases.csv')
    # df1 = pd.DataFrame(columns=['case', 'solver1', 'solver2', 'solver3'])
    # df1.to_csv('./Diff.csv')
    # df = pd.DataFrame(columns=['nax_str_len', 'var_num', 'assert_num', 'max_depth', 'average_time'])
    # df.to_csv('./Parameter.csv')


    main()