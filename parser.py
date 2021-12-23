import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--solvers",
                metavar="solvers[solver1,solver2,...]",
                action="store",
                # type = str,
                dest="solvers",
                default=[],
                nargs='+',
                help="The target SMT Solvers for SPRFinder."
)
parser.add_argument("-t", "--type",
                metavar="z3seq, z3str3 or cvc4",
                action="store",
                type = str,
                dest='type',
                default='',
                nargs=1,
                help="The type of the solver."
)

parser.add_argument('-l', '--string_length',
                    metavar="length",
                    action="store",
                    type = int,
                    dest="length",
                    default=10,
                    help="The init max string length"
                    )

parser.add_argument('-v', '--var_num',
                    metavar="-v var_num",
                    action="store",
                    type = int,
                    dest="var_num",
                    default=3,
                    help="The init max variable number"
                    )
parser.add_argument('-a', '--assert_num',
                    metavar="-a assert_num",
                    action="store",
                    type = int,
                    dest="assert_num",
                    default=4,
                    help="The init max assert number"
                    )
parser.add_argument('-d', '--max_depth',
                    metavar="-d init_depth",
                    action="store",
                    type = int,
                    dest="depth",
                    default=3,
                    help="The init max depth"
                    )

parser.add_argument('-T' '--time_out',
                    metavar='-T time',
                    action='store',
                    dest='timeout',
                    default=20,
                    help='The timeout setting'
                    )
args = parser.parse_args()
