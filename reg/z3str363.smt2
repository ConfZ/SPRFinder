(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (> var0 var1))
(assert (str.prefixof (str.replace (str.at var2 var3) (str.at var4 var5) (str.replace var6 var7 var2)) (str.substr var7 var1 120)))
(assert (> (str.len var6) (str.to.int var2)))
(assert (str.in.re (str.replace var4 var4 var7) (re.* re.allchar)))
(check-sat)