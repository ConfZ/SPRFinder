import os, random, time
import src.settings as settings
from src.smtlib.script import SMTLIBScript
from src.solver import run_solver
import pandas as pd
# from src.parser import args

def par2(x):
    if x < settings.timeout:
        return x
    else:
        return settings.timeout


def generate_file(ast, path, name):
    # with open(path, 'w+') as file:
    if not os.path.exists(path):
        os.mkdir(path)
    file = open(os.path.join(path, name), 'w+')
    file.write(ast)
    file.close()


class Instance(SMTLIBScript):
    def __init__(self, val=None, statistics=None):
        if settings.theory == 'QF_S' or settings.theory == 'QF_SLIA':
            assert isinstance(val, str)
        else:
            assert isinstance(val, list)
        super().__init__()
        # self.para = para
        self.statistics = statistics
        self.primaries = val
        self.times = {}
        self.results = {}
        self.name = str(time.time()).replace(".", "") + str(os.getpid()) + str(random.randint(0, 99999999)) + ".smt2"
        self.err_log = {}
        self._score = None
        self.time_list = [0, 0, 0]
    def solve(self):
        for solver in settings.solvers:
            out, time, dump = run_solver(self, solver, settings.mode)
            self.results[solver] = out
            self.times[solver] = par2(time)
            if out is 'err': self.err_log[solver] = dump

    # if len(self.err_log) > 0:
    # 	self.to_file(settings.db + '/crashes/')

    def score(self):
        if self._score != None: return self._score
        if self.inconsistent():
            # generate_file(str(self), '../Diff', 'diff' + str(settings.diff_num) + '.smt2')
            # df = pd.DataFrame(['diff' + str(settings.diff_num) + '.smt2', self.results[settings.solvers[0]],
            #                    self.results[settings.solvers[1]], self.results[settings.solvers[2]]]).T
            # df.to_csv('./Diff.csv', mode='a', header=False)
            # settings.diff_num += 1
            self._score = par2(self.times[settings.solvers[0]]) - min(
                [par2(self.times[solver]) for solver in settings.solvers if solver != settings.solvers[0]])
        elif settings.BugMode:
            self._score = 0.0
        elif len(self.err_log) > 0:
            self._score = 0.0
        elif len(self.times) == 1:
            self._score = par2(self.times[settings.solvers[0]]) if settings.solvers[0] not in self.err_log else float(
                '-inf')
        else:
            print('solvers:', settings.solvers)
            self._score = par2(self.times[settings.solvers[0]]) - min(
                [par2(self.times[solver]) for solver in settings.solvers if solver != settings.solvers[0]])
        return self._score

    def __lt__(self, other):
        return self.score() < other.score()

    def __str__(self):
        return self.primaries

    __repr__ = __str__

    def inconsistent(self):
        for solver in self.results:
            clean = ""
            for i in range(len(self.results[solver])):
                if self.results[solver][i].isalpha():
                    clean = clean + self.results[solver][i]
            self.results[solver] = clean
        ans = ""
        says_sat = False
        says_unsat = False
        for solver in self.results:
            if self.results[solver] == "sat":
                says_sat = True
            if self.results[solver] == "unsat":
                says_unsat = True
        return says_sat and says_unsat

