(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (<= (str.indexof var0 var1 var2) (str.to.int (str.at var3 var4))))
(assert (str.prefixof var5 var3))
(assert (str.suffixof (str.substr var3 var6 var7) (str.substr var1 var2 var7)))
(assert (>= (str.indexof var0 var5 var4) (str.len (str.at var0 var2))))
(check-sat)