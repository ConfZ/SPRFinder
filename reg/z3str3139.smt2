(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (< (str.to.int var0) (str.len var1)))
(assert (< var2 var3))
(assert (<= var4 var5))
(assert (str.suffixof (str.at var6 var2) (str.substr var7 12 var3)))
(check-sat)