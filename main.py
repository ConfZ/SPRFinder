import os
import settings
import random
import fuzzer
import pandas as pd
import time
import parser

def delete_cases(path):
    if os.path.exists(path):
        for fpath, _, file_list in os.walk(path):
            for fname in file_list:
                if fname.endswith('.smt2'):
                    os.remove(os.path.join(fpath, fname))
        print('have deleted ', path)

def main():
    settings.timeout = 20
    settings.GeneratorMaxDepth =  6
    settings.GeneratorNumConst =   20
    settings.NumAssert = 15
    settings.MaxStr = 500
    settings.MinStr = 10

    settings.max_var_num = 3
    settings.max_assert_num = 4
    settings.max_depth = 3
    settings.max_str_len = 10
    settings.reg_path = './reg'
    settings.non_reg_path = 'non-reg'
    settings.string_ops = [
        # 'and','or','not','=','
        'Concat', 'Contains', 'Length', 'IndexOf', 'IndexOf2', 'PrefixOf', 'SuffixOf', 'Replace', 'Substring',
        'FromInt', 'ToInt',
        # 'InRegex','At',
        'Str2Re', 'ReConcat', 'ReStar', 'RePlus', 'ReRange', 'ReUnion', 'ReInter'
    ]
    settings.mode = 'cvc4'
    settings.solver_type = settings.mode
    settings.theory = 'QF_SLIA'
    settings.file_name = settings.mode
    if settings.mode == 'cvc4':
        solvers = ['/home/marui18b/zy/cvc4_version/CVC4-1.9/build/bin/cvc4',
                   '/home/marui18b/zy/cvc4_version/CVC4-1.8/build/bin/cvc4',
                   '/home/marui18b/zy/cvc4_version/CVC4-1.7/build/bin/cvc4']
        # solvers = ['//home/zy/Documents/smt_editions/cvc4_editions/CVC4-1.9/build/bin/cvc4',
        #            '/home/zy/Documents/smt_editions/cvc4_editions/CVC4-1.8/build/bin/cvc4',
        #            '/home/zy/Documents/smt_editions/cvc4_editions/CVC4-1.7/build/bin/cvc4']

    elif settings.mode == 'z3str3' or settings.mode == 'z3seq':
        # solvers = ['/home/zy/Documents/smt_editions/z3_editions/z3-4.8.9/build/z3-4.8.9',
        #            '/home/zy/Documents/smt_editions/z3_editions/z3-4.8.8/build/z3',
        #            '/home/zy/Documents/smt_editions/z3_editions/cmt1/build/z3']
        solvers = ['/home/marui18b/zy/z3_version/z3-4.8.9/build/z3',
                   '/home/marui18b/zy/z3_version/z3-4.8.8/build/z3',
                   '/home/marui18b/zy/z3_version/z3-4.8.7/build/z3']
    elif settings.mode == 'commit':
        solvers = settings.commits
    else:
        assert False, 'wrong mode'
    for solver in solvers:
        assert os.path.isfile(solver), "No path to: " + solver
    settings.solvers = list(solvers)
    finder = fuzzer.Fuzzer(time.time())
    finder.run()
    # settings.pre_name = 's5_t5'

if __name__ == '__main__':

    print(os.getcwd())
    df = pd.DataFrame(columns=['time', 'case_number'])
    df.to_csv('./Statistics.csv')
    df1 = pd.DataFrame(columns=['case', 'solver1', 'solver2', 'solver3', 'var_num', 'assert_num', 'nax_str_len', 'max_depth'])
    df1.to_csv('./Results.csv')
    df1 = pd.DataFrame(columns=['case', 'solver1', 'solver2', 'solver3'])
    df1.to_csv('./Diff.csv')
    df = pd.DataFrame(columns=['nax_str_len', 'var_num', 'assert_num', 'max_depth', 'average_time'])
    df.to_csv('./Parameter.csv')
    delete_cases(settings.reg_path)
    delete_cases(settings.non_reg_path)
    main()