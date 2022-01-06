import os

import settings
from settings import flag
from executor import run_command, run_solver
import utils



# def getcmd(cmd):
#     proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     try:
#         start = time.time()
#         text, err = proc.communicate(timeout=600)
#         if err:
#             text = 'err occured!'
#             err = str(err)
#         end = time.time()
#         runtime = start - end
#     except subprocess.TimeoutExpired:
#         runtime = settings.timeout
#         text = 'timeout'
#         err = None
#     return str(text), err, runtime


class Case:
    def __init__(self, file, t_pre, t_post):
        self.type = settings.solver
        self.find_err = False
        # print(file, ':', settings.case_path)
        self.file = os.path.join(settings.case_path, file)
        self.direction = 0  # going up or going down
        # self.pair = pair
        self.path = settings.init_path
        self.ahead = True
        self.run_time = 0
        # self.is_err = False
        self.flag = None
        self.mid = False
        self.t_s = t_pre
        self.t_e = t_post
        self.t_pre = t_pre
        self.t_post = t_post
        self.target_cmt = []
        self.is_reg = True
        self.negative_cmt = []
        # print(self.type)
        if self.type == 'cvc4':
            self.cmd = 'timeout {} ./cvc4 --strings-exp '.format(settings.timeout)
        elif self.type == 'seq':
            self.cmd = 'timeout {} ./z3 smt.string_solver=seq'.format(settings.timeout)
        elif self.type == 'z3str3':
            self.cmd = 'timeout {} ./z3 smt.string_solver=z3str3'.format(settings.timeout)
        else:
            raise ValueError('cvc4, seq or z3str3')
        self.delta = (self.t_post-self.t_pre)/4
        if self.delta < 5:
            self.delta = 5

    # def init_run(self):
    #     os.chdir(self.path)
    #     os.system('git reset --hard ' + self.pair[0])
    #     utils.goto_path(os.path.join(os.getcwd(), 'build'))
    #     os.system('make clean')
    #     os.system('cmake ..')
    #     os.system('make -j5')
    #     if type == 'cvc4':
    #         os.chdir(os.path.join(os.getcwd(), 'bin'))
    #     err0, self.t_pre = self.run4time(self.cmd + self.file)
    #     os.chdir(self.path)
    #     os.system('git reset --hard ' + self.pair[1])
    #     utils.goto_path(os.path.join(os.getcwd(), 'build'))
    #     os.system('cmake ..')
    #     os.system('make -j5')
    #     err1, self.t_post = self.run4time(self.cmd + self.file)
    #     if self.t_post <= self.t_pre or err1 is not None or err0 is not None:
    #         self.is_reg = True
    #     else:
    #         self.is_reg = False
    def update_delta(self):
        self.delta = (self.t_post-self.t_pre)/4
        if self.delta < 5:
            self.delta = 5

    def set_tpre(self, t):
        self.t_pre = t

    def set_tpost(self, t):
        self.t_post = t

    def run4time(self, cmd):
        _, err, runtime = run_command(cmd)
        return err, runtime

    # def set_good(self):
    #     self.commit[1] = settings.current_cmt
    #
    def run(self):
        os.chdir(os.path.join(self.path, 'build'))
        if self.type == 'cvc4':
            os.chdir(os.path.join(os.getcwd(), 'bin'))
        rtext, rerr, rtime = run_solver(self.cmd, self.file)
        if rtext.lower().find('sat'):
            print('result: sat')
        elif rtext.lower().find('unsat'):
            print('result: unsat')
        if rerr.lower().find("segmentation") != -1:
            self.find_err = True
        else:
            self.run_time = rtime
            if rtime - self.t_pre <= self.delta and rtime - self.t_pre <= self.t_post - rtime:
                if rtime < self.t_pre:
                    self.t_pre = rtime
                self.flag = flag.good
                # self.pair[0] = settings.current_cmt

            elif self.t_post - rtime <= self.delta:
                if rtime > self.t_post:
                    self.t_post = rtime
                self.flag = flag.bad
                # self.pair[1] = settings.current_cmt
                self.find_err = False
            # elif self.t_post - self.delta > rtime and self.delta - self.t_pre < rtime:
            elif self.t_post - rtime > self.delta and rtime - self.t_pre > self.delta:
                # self.t_pre = rtime
                # self.pair[1] = settings.current_cmt
                self.flag = flag.mid
            else:
                self.flag = None

