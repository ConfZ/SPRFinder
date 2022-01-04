# SPRFinder
Performance regression testing tool for SMT string solvers;


## Performance Regression Detecting

+ bash build_all.sh
+ cd path of SPRFinder
+ python3 bin/SPRFinder.py -t solver_type (z3seq, z3str3 or cvc4) -s path_of_latest_solver path_of_solver1 ...

The regression cases can be found at ./results/Regression_cases
The Statistics can be found at ./results/Statistics

## SPR Localization


+ Please clone the CVC4 code or Z3 code to the file ./src/auto_cmt

cd ./src/auto_cmt

git clone https://github.com/Z3Prover/z3.git
