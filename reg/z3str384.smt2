(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(assert (str.prefixof (str.replace var0 var1 var2) (str.replace var3 var1 var2)))
(assert (str.contains var2 var1))
(assert (<= (str.len var1) (str.len var2)))
(assert (>= var4 62))
(check-sat)