import settings
from Case import Case
import cmt_checker
import utils
import os
from git_bisect import Bisect
from csv_parser import parse_csv, get_commit_list
from settings import flag
import pandas as pd
from init_run import init_run
from parser import args
def init_settings(para):

def main():
    # parse_csv(settings.csv_path)
    init_run()
    if any([settings.solver == 'seq', settings.solver == 'z3str3']):
        commit_pre = settings.z3_versions['z3-4.8.7']
        commit_post = settings.z3_versions['z3-4.8.9']
    elif settings.solver == 'cvc4':
        commit_pre = settings.cvc4_versions['cvc4-1.7']
        commit_post = settings.cvc4_versions['cvc4-1,9']
    else:
        raise ValueError('solver should be cvc4, seq, or z3str3')
    # print(get_commit_list(commit_pre, commit_post))
    get_commit_list(commit_pre, commit_post)
    # print('settings_cmt:', settings.commits)
    log = settings.commits
    settings.commit_log = dict(zip(log, [1 for _ in log]))
    # files = utils.iter_path('./cases')
    # cmt_case = []
    # cases = []
    # for file in files:
    #     case = Case.Case(file, commit_pre, commit_post)
    #     case.init_run()
    #     cases.append(case)
    cmt_case_stack = []
    for key in settings.cmt_case:
        cmt_case_stack.append([utils.key2pair(key), settings.cmt_case[key]])
    while len(cmt_case_stack) > 0:
        pair = cmt_case_stack[0][0]
        cases = cmt_case_stack[0][1]
        cmt_case_stack.pop(0)
        # print(pair)
        bisect = Bisect(pair)
        if bisect.bisect_fault:
            continue
        print('bisect_commit:', bisect.commits)
        bisect.propagate()
        while not bisect.is_find:
            success = bisect.build()
            if not success:
                bisect.deal_with_build_error()
            good_case = []
            bad_case = []
            for c in cases:
                c.pair = [bisect.commits[0], bisect.commits[-1]]
                c.run()
                # if c.flag == flag.run_error:
                #     bisect.deal_with_run_error(c)
                if c.flag == flag.good:
                    good_case.append(c)
                elif c.flag == flag.bad:
                    bad_case.append(c)
                elif c.flag == flag.mid:
                    # if c.t_post - c.run_time >= 10:
                    if c.run_time - c.t_pre > 10:
                        new_case_good = Case(c.file, c.run_time, c.t_post)
                        new_case_good.flag = flag.good
                        good_case.append(new_case_good)
                    if c.t_post - c.run_time > 10:
                    # if c.run_time - c.t_pre >= 10:
                        new_case_bad = Case(c.file, c.t_pre, c.run_time)
                        new_case_bad.flag = flag.bad
                        bad_case.append(new_case_bad)
                else:
                    continue

                    # c.t_pre = c.run_time
                    # c.pair[0] = settings.current_cmt
                    # # print(c.file, bisect.commits)
                    # new_case = Case(c.file, c.t_pre, c.run_time)
                    # c.t_pre = c.run_time
                    # new_case.flag = flag.bad
                    # new_case.delta = c.delta
                    # good_case.append(c)
                    # bad_case.append(new_case)
            if len(good_case) >= len(bad_case):
                cases = good_case
                if len(bad_case) > 0:
                    cmt_case_stack.append([[bisect.commits[0], bisect.current], bad_case])
                bisect.mark(flag.good)
            else:
                cases = bad_case
                if len(good_case) > 0:
                    cmt_case_stack.append([[bisect.current, bisect.commits[-1]], good_case])
                bisect.mark(flag.bad)
            bisect.propagate()
            if bisect.is_find:
                settings.unique_cmt += 1
                if settings.commit_log[bisect.current] == '0':
                    build_error = 'Y'
                else:
                    build_error = ' '
                for case in cases:
                    print('writing to the log!')
                    if case.find_err:
                        find_error = 'Y'
                    else:
                        find_error = ' '
                    df1 = pd.DataFrame([case.file, bisect.current, build_error, find_error, settings.unique_cmt]).T
                    df1.to_csv(os.path.join(settings.root_path, 'Location.csv'), mode='a', header=False)
        settings.have_found_dict[bisect.current] = cases
    os.chdir(settings.init_path)

    good_cmt = '\n'.join(settings.commits)
    good_log = open(os.path.join(settings.root_path, './good_log'), 'w+')
    good_log.write(good_cmt)
    good_log.close()



# if __name__ == '__main__':
#     df = pd.DataFrame(columns=['case', 'commit', 'build_error', 'find_error', 'unique_cmt'])
#     df.to_csv('./Location.csv')
#     settings.solver = args.solver[0]
#     if settings.solver == 'z3seq':
#         settings.solver = 'seq'
#
#     father_path = os.path.dirname(os.getcwd())
#     settings.father_path = father_path
#     if settings.solver == 'seq' or settings.solver == 'z3str3':
#         settings.solvers = ['/home/marui18b/zy/z3_version/z3-4.8.9/build/z3',
#                    '/home/marui18b/zy/z3_version/z3-4.8.8/build/z3',
#                    '/home/marui18b/zy/z3_version/z3-4.8.7/build/z3']
#     elif settings.solver == 'cvc4':
#         settings.solvers = ['/home/marui18b/zy/cvc4_version/CVC4-1.9/build/bin/cvc4',
#                    '/home/marui18b/zy/cvc4_version/CVC4-1.8/build/bin/cvc4',
#                    '/home/marui18b/zy/cvc4_version/CVC4-1.7/build/bin/cvc4']
#     # settings.solvers = ['/home/zy/Documents/smt_editions/z3_editions/z3-4.8.9',
#     #                     '/home/zy/Documents/smt_editions/z3_editions/z3-4.8.8',
#     #                     '/home/zy/Documents/smt_editions/z3_editions/z3-4.8.7']
#     # print('solver is', settings.solver)
#     if any([settings.solver == 'seq', settings.solver == 'z3str3']):
#         tool_file = 'z3'
#     elif settings.solver == 'cvc4':
#         tool_file = 'CVC4'
#     else:
#         raise ValueError('solver should be cvc4, seq, or z3str3')
#     # print(os.getcwd())
#     settings.root_path = os.getcwd()
#     # father_path = os.path.dirname(os.getcwd())
#     # settings.case_path = os.path.join(father_path, 'BanditFuzz_beta', 'cases')
#     # settings.init_path = os.path.join(father_path, 'Localize', tool_file)
#     # settings.csv_path = os.path.join(father_path, 'BanditFuzz_beta', 'Results.csv')
#     if len(args.cases[0]) == 0:
#         settings.case_path = os.path.join(os.getcwd(), 'cases')
#     else:
#         settings.case_path = args.cases[0]
#     settings.init_path = os.path.join(os.getcwd(), tool_file)
#     settings.csv_path = os.path.join(os.getcwd(), 'Results.csv')
#
#     main()
#     print('have finished!')
