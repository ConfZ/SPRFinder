(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.suffixof (str.substr var0 var1 var2) (str.replace var3 var4 var5)))
(assert (>= var6 var7))
(assert (<= var2 var7))
(assert (str.contains (str.replace var4 var0 var5) (str.replace var4 var0 var5)))
(check-sat)