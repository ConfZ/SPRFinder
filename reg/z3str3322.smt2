(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(assert (> (str.indexof var0 "x)k_'" var1) (str.to.int var2)))
(assert (str.prefixof (str.substr var3 var4 178) (str.replace var5 var2 var0)))
(assert (str.in.re var5 re.allchar))
(assert (str.in.re (str.at "Uw*m]u][" var6) (re.inter re.allchar re.allchar)))
(check-sat)