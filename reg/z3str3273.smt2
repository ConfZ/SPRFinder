(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(assert (str.suffixof (str.replace var0 var1 var2) (str.replace var3 var3 var0)))
(assert (> (str.len var0) (str.to.int var1)))
(assert (not (<= (str.len var2) (str.indexof var3 var2 var4))))
(assert (str.prefixof (str.replace var1 var1 var2) (str.at var1 var5)))
(check-sat)