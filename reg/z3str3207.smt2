(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.prefixof (str.at var0 var1) (str.replace var2 var3 var4)))
(assert (not (str.in.re var4 re.allchar)))
(assert (str.in.re (str.substr var4 var5 var6) (re.+ re.allchar)))
(assert (>= var7 var6))
(check-sat)