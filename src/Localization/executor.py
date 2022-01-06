import time
import subprocess
import tempfile
import settings
def run_command(command):
    start = time.time()
    print('cmd:', command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    proc_stdout, proc_stderr = process.communicate()
    print('out:', proc_stdout)
    print('error:', proc_stderr)
    wall_time = time.time() - start

    proc_stdout = proc_stdout.decode('utf-8').strip()
    proc_stderr = proc_stderr.decode('utf-8').strip()
    out_lines = str(proc_stdout)
    err_lines = str(proc_stderr)
    if out_lines.lower().find('sat'):
        print('result: sat')
    elif out_lines.lower().find('unsat'):
        print('result: unsat')

    return out_lines, err_lines, wall_time

def run_solver(cmd, file):
    rout, rerr, rtime = run_command('{} {}'.format(cmd, file))
    print('cmd:', cmd)
    if settings.solver == 'cvc4':
        if rout.lower().find('error') != -1:
            with open(file, 'r') as f:
                case_former = f.read()
                f.close()

            tfile = tempfile.NamedTemporaryFile(delete=True, suffix='.smt2')
            case_former = case_former.replace('str.from.int', 'str.from_int')
            case_former = case_former.replace('str.in.re', 'str.in_re')
            case_former = case_former.replace('str.to.int', 'str.to_int')
            case_former = case_former.replace('str.to.re', 'str.to_re')
            outFile = open(tfile.name, 'w')
            outFile.write(str(case_former))
            outFile.close()
            rout, rerr, rtime = run_command('{} {}'.format(cmd, outFile.name))
    print('out:', rout)
    print('error:', rerr)
    return rout,rerr, rtime