(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.in.re var0 re.allchar))
(assert (str.in.re (str.replace (str.replace "(gq" var1 var2) (str.at var3 var4) (str.at var1 var5)) (re.+ (re.+ re.allchar))))
(assert (str.suffixof (str.replace var0 var1 var1) (str.substr var3 87 47)))
(assert (str.contains (str.replace var2 "!b" var1) (str.substr var2 var6 var7)))
(check-sat)