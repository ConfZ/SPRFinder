import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target-solver",
                metavar="The solver path (z3 or CVC4)",
                action="store",
                type = str,
                dest="solver",
                default='seq',
                # nargs=1,
                required=True,
                help="The target SMT Solvers in the banditfuzz loop."
)
parser.add_argument("-s", "--solver-versions",
                metavar='versions[latest version, earlier version1,...]',
                action="store",
                type = str,
                dest="versions",
                default=[],
                nargs='+',
                required=True,
                help="The target SMT versions in the BanditFuzz loop."
)
parser.add_argument("-c", "--cases",
                metavar="case_path",
                action="store",
                type = str,
                dest="cases",
                default='',
                # nargs=1,
                required=True,
                help="The path of the target cases."
)
args = parser.parse_args()
