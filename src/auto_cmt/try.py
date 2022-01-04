# import math
# from git_bisect import Bisect
# from settings import flag
# import time
from executor import run_command
# import subprocess
# def run_command(command):
#
#     start = time.time()
#     process = subprocess.Popen(command,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     print('cmd:', command)
#     proc_stdout,proc_stderr = process.communicate()
#     print('error:', proc_stderr)
#     wall_time = time.time() - start
#
#
#     proc_stdout = proc_stdout.decode('utf-8').strip()
#     proc_stderr = proc_stderr.decode('utf-8').strip()
#     out_lines = str(proc_stdout)
#     err_lines = str(proc_stderr)
#
#     return out_lines,err_lines,wall_time
if __name__ == '__main__':
    rout, rerr, rtime = run_command('git reset --hard 95ee5fa68')
    print('out:\n', rout)
    print('err:\n', rerr)


