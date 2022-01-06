import pandas as pd
import settings
import utils
from math import ceil
from Case import Case
import os
def add_to_set(pair, file):
    if utils.pair2key(pair) not in settings.cmt_case.keys():
        settings.cmt_case[utils.pair2key(pair)] = [file]
    else:
        settings.cmt_case[utils.pair2key(pair)].append(file)
def parse_csv(path):
    if settings.solver == 'cvc4':
        cmt1 = settings.cvc4_versions['cvc4-1.9']
        cmt2 = settings.cvc4_versions['cvc4-1.8']
        cmt3 = settings.cvc4_versions['cvc4-1.7']

    elif settings.solver == 'z3str3' or settings.solver == 'seq':
        cmt1 = settings.z3_versions['z3-4.8.9']
        cmt2 = settings.z3_versions['z3-4.8.8']
        cmt3 = settings.z3_versions['z3-4.8.7']


    else:
        raise ValueError('solver should be cvc4 or z3str3 or seq')
    df = pd.read_csv(path, header=0)
    # print(df['case'].tolist())
    files = list(df['case'])
    solver1 = list(df['solver1'])
    solver2 = list(df['solver2'])
    solver3 = list(df['solver3'])
    for i in range(len(files)):


        if ceil(solver1[i]) - ceil(solver2[i]) > ceil(solver2[i]) - ceil(solver3[i]):
            case = Case(files[i], solver2[i], solver1[i])
            # case.set_tpre(solver2[i])
            # case.set_tpost(solver1[i])
            add_to_set([cmt2, cmt1], case)
        else:
            case = Case(files[i], solver3[i], solver2[i])
            # case.set_tpre(solver3[i])
            # case.set_tpost(solver2[i])
            add_to_set([cmt3, cmt2], case)

def get_commit_list(pre=None, post=None):
    os.chdir(settings.root_path)
    file = open('./log.log', 'r')
    tmp = file.read()
    file.close()
    commits = tmp.split('\n')
    commits.reverse()
    if pre is not None and pre in commits:
        pre_index = commits.index(pre)
    else:
        pre_index = 0
    if post is not None and post in commits:
        post_index = commits.index(post)+1
    else:
        post_index = len(commits)
    settings.commits = commits[pre_index:post_index]
    return commits[pre_index:post_index]


