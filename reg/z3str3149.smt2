(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (>= (str.len var0) (str.to.int var1)))
(assert (>= (str.indexof var2 var3 var4) (str.to.int var0)))
(assert (str.prefixof (str.substr var3 var5 var6) (str.at var1 var7)))
(assert (str.suffixof var2 var3))
(check-sat)