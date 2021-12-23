import os
import sys

if __name__ == '__main__':
    smt_tool = sys.argv[1]
    assert smt_tool == 'cvc4' or smt_tool == 'z3', 'please type in cvc4 or z3'
    os.chdir(os.path.join(os.getcwd(), smt_tool))
    os.system(r'rm -f ./.git/index.lock')
    os.system('git checkout master')