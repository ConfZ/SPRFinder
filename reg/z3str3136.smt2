(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.suffixof (str.substr var0 var1 var2) (str.at (str.replace "%sPD&j" var3 "utOlcn\\""}") (str.to.int var4))))
(assert (str.in.re var5 re.allchar))
(assert (< (str.len var3) (str.to.int var5)))
(assert (<= var6 var7))
(check-sat)