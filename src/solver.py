import subprocess, time, tempfile
import src.settings as settings


def run_command(command):
    start = time.time()
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, encoding='utf-8')
    print('cmd:', command)
    proc_stdout, proc_stderr = process.communicate()
    # print('error:', proc_stderr)
    wall_time = time.time() - start

    proc_stdout = proc_stdout
    proc_stderr = proc_stderr
    out_lines = str(proc_stdout)
    err_lines = str(proc_stderr)
    # print('process_out:', out_lines)
    return out_lines, err_lines, wall_time

def run_solver(instance, solver, type='z3str3'):
    tfile = tempfile.NamedTemporaryFile(delete=True, suffix='.smt2')
    if type == 'z3str3':
        op = 'smt.string_solver=' + type
    elif type == 'z3seq':
        op = 'smt.string_solver=' + 'seq'
    elif type == 'fp':
        op = ''
    elif type == 'cvc4':
        op = '--strings-exp'

    else:
        op = ''
    case_former = str(instance)
    if solver.find('CVC4-1.7')== -1 or solver.find('cvc4-1.7') == -1:
        case_former = case_former.replace('str.from.int', 'str.from_int')
        case_former = case_former.replace('str.in.re', 'str.in_re')
        case_former = case_former.replace('str.to.int', 'str.to_int')
        case_former = case_former.replace('str.to.re', 'str.to_re')
        case_former = case_former.replace('str.from.int', 'str.from_int')
    print('case_former:', case_former)
    outFile = open(tfile.name, 'w')
    outFile.write(str(case_former))
    outFile.close()
    out, err, time = run_command(
        "timeout " + str(settings.timeout + 1) + " bash -c \'" + solver + ' ' + op + " " + outFile.name + '\'')
    # if out.lower().find('error') != -1:
    #     case_former = case_former.replace('str.from.int', 'str.from_int')
    #     case_former = case_former.replace('str.in.re', 'str.in_re')
    #     case_former = case_former.replace('str.to.int', 'str.to_int')
    #     case_former = case_former.replace('str.to.re', 'str.to_re')
    #
    #     outFile = open(tfile.name, 'w')
    #     outFile.write(str(case_former))
    #     outFile.close()
    #     out, err, time = run_command(
    #         "timeout " + str(settings.timeout + 1) + " bash -c \'" + solver + ' ' + op + " " + outFile.name + '\'')

    print('instance:', instance)
    print('solver:', solver)
    print('run time:', time)
    print('out:', out)
    print('err', err)
    if time > settings.timeout:
        # settings.all_run_time.append(time)
        settings.average_time[1] += 1
        settings.average_time[0] = (settings.average_time[0] + time) / settings.average_time[1]
        print(settings.average_time)
        return 'timeout', time, out + err
    if out.lower().find('sat') != -1 or out.lower().find('unsat') != -1:
        # settings.all_run_time.append(time)
        settings.average_time[1] += 1
        settings.average_time[0] = (settings.average_time[0] + time) / settings.average_time[1]
        print(settings.average_time)
        return out.lower(), time, out + err
    return 'err', time, out + err

# start = time.time()
# out = subprocess_cmd(cmd)
# instance.times[solver_name] = min(time.time() - start,settings.SolverTimeout)
# instance.results[solver_name] = out
# if out != "err" and out != "sat" and out != "unsat" and instance.times[solver_name] >= settings.SolverTimeout:
# 	instance.results[solver_name] = "timeout"

# if not (instance.results[solver_name] == 'sat' or instance.results[solver_name] == 'unsat'):
# 	instance.times[solver_name] = settings.SolverTimeout

# os.remove('/tmp/' + instance.name)
