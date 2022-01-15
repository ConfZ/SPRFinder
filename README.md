# SPRFinder
This project is a Performance regression testing tool for SMT string solvers. 

This project consists of two sections: 1) The performance Regression Detecting; 2) SPR Localization. 

Please refer to our website for more information on this project and can also find the results of our experiment.
Webset of SPRFinder: https://sites.google.com/view/sprfinder/home

The SPR-inducing cases found by SPRFinder: https://github.com/ConfZ/all_regressions.git



## Performance Regression Detecting

+ First install the dependence by.
```
$pip3 install dtw-python
```

### Optional Arguments:
```
//Settings for fuzzer

-h show the help message of SPRFinder.
-t, --type [z3seq/z3str3/cvc4] The name of the target solver. (default: none)
-s, --solver-versions [latest version, earlier version1,...] The different versions of the target solver. (default: none)
-T, --time_out [time(s)]  The timeout setting for each running of test cases.

//Settings for generator

-l --string_length [val]  The initial max string length for the generator. (default: 10)
-v --var_num       [val]  The initial max variable number for the generator. (default: 3)
-a --assert_num    [val]  The initial max assert number for the generator. (default: 4)
-d --max_depth     [val]  The initial max assert number for the generator. (default: 3)
```

### Run
+ For example, detecting SPR on the versions of z3-seq.

```
$cd path of SPRFinder
$python3 bin/SPRFinder.py -t z3seq -s z3-4.8.9 z3-4.8.8 z3-4.8.7
```

The regression cases can be found at ./results/Regression_cases
The Statistics can be found at ./results/Statistics

## SPR Localization


+ Clone the CVC4 code or Z3 code to the file ./src/auto_cmt

```
$cd ./src/auto_cmt

$git clone https://github.com/Z3Prover/z3.git
```
### Optional Arguments:

```
-t, --type [z3seq/z3str3/cvc4] The name of the target solver. (default: none)
-s, --solver-versions [latest version, earlier version1,...] The different versions of the target solver. (default: none)
-T, --time_out [time(s)]  The timeout setting for each running of test cases.
```

+ Please keep your network online.
+ Run:

For example, conduct the localization on z3seq.
```
$cd Path_of_SPRFinder
$python3 bin/Localization.py -t z3seq -s z3-4.8.9 z3-4.8.8 z3-4.8.7
```

The results can be find at ./results/Localized


