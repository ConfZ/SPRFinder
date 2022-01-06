import settings
import utils
from math import ceil
from Case import Case
import os
from executor import run_command


def add_to_set(pair, file):
    if utils.pair2key(pair) not in settings.cmt_case.keys():
        settings.cmt_case[utils.pair2key(pair)] = [file]
    else:
        settings.cmt_case[utils.pair2key(pair)].append(file)


def init_run():
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
    files = utils.iter_path(settings.case_path)
    for file in files:
        rout1, rerr1, rtime1 = run_command(
            'timeout {} {} smt.string_solver={} {}'.format(settings.timeout, settings.solvers[0], settings.solver,
                                                              file))
        rout2, rerr2, rtime2 = run_command(
            'timeout {} {} smt.string_solver={} {}'.format(settings.timeout, settings.solvers[1], settings.solver,
                                                              file))
        rout3, rerr3, rtime3 = run_command(
            'timeout {} {} smt.string_solver={} {}'.format(settings.timeout, settings.solvers[2], settings.solver,
                                                              file))
        if any([rerr1.find('segmentation') != -1, rerr2.find('segmentation') != -1, rerr3.find('segmentation') != -1]):
            continue
        else:
            if rtime1 - rtime2 >= 10:
                case = Case(file, rtime2, rtime1)
                add_to_set([cmt2, cmt1], case)
            if rtime2 - rtime3 >= 10:
                case = Case(file, rtime3, rtime2)
                add_to_set([cmt3, cmt2], case)
