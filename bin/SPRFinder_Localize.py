
import os
from pathlib import Path
import sys
import pandas as pd
path = Path(__file__)
root_path = path.parent.absolute().parent
sys.path.append(str(root_path))
# sys.path.append(str(root_path / 'src'))
from src.Localization.parser import args
from src.Localization.settings import parameters
from src.Localization.Localize import localize
# print(root_path)



if __name__ == '__main__':
    df = pd.DataFrame(columns=['case', 'commit', 'build_error', 'find_error', 'unique_cmt'])
    df.to_csv(str(root_path/'src'/'Localization'/'results'/'Location.csv'))
    para = parameters()
    para.solver = args.solver
    if para.solver == 'z3seq':
        para.solver = 'seq'

    # father_path =
    para.root_path = str(root_path/'src'/'Localization')
    para.solvers = args.versions
    # settings.solvers = ['/home/zy/Documents/smt_editions/z3_editions/z3-4.8.9',
    #                     '/home/zy/Documents/smt_editions/z3_editions/z3-4.8.8',
    #                     '/home/zy/Documents/smt_editions/z3_editions/z3-4.8.7']
    # print('solver is', settings.solver)
    if any([para.solver == 'seq', para.solver == 'z3str3']):
        tool_file = 'z3'
    elif para.solver == 'cvc4':
        tool_file = 'CVC4'
    else:
        raise ValueError('solver should be cvc4, seq, or z3str3')
    # print(os.getcwd())
    # para.root_path = os.getcwd()
    # father_path = os.path.dirname(os.getcwd())
    # settings.case_path = os.path.join(father_path, 'BanditFuzz_beta', 'cases')
    # settings.init_path = os.path.join(father_path, 'Localization', tool_file)
    # settings.csv_path = os.path.join(father_path, 'BanditFuzz_beta', 'Results.csv')
    if len(args.cases[0]) == 0:
        para.case_path = str(root_path/'results'/'Regression_cases')
    else:
        para.case_path = args.cases[0]
    para.init_path = os.path.join(para.root_path, tool_file)
    para.csv_path = str(root_path/'results/Statistics/Regression_number.csv')

    localize(para)
    print('have finished!')