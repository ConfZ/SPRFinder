(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Bool)
(declare-fun var7 () String)
(declare-fun var8 () String)
(assert (str.suffixof (str.substr var0 var1 var2) (str.at var3 var4)))
(assert (<= var5 var5))
(assert (not var6))
(assert (< (str.to.int var7) (str.len var8)))
(check-sat)