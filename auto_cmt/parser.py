import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target-solvers",
                metavar="z3seq, z3str3, cvc4",
                action="store",
                type = str,
                dest="solver",
                default='seq',
                nargs=1,
                help="The target SMT Solvers in the banditfuzz loop."
)
parser.add_argument("-c", "--cases",
                metavar="case_path",
                action="store",
                type = str,
                dest="cases",
                default='',
                nargs=1,
                help="The path of the target cases."
)
args = parser.parse_args()
