(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (> var0 var1))
(assert (str.suffixof (str.replace var2 var3 var4) (str.substr var5 var6 var7)))
(assert (<= (str.indexof var3 var2 var7) (str.indexof (str.substr var2 var0 var7) (str.substr var3 var1 var0) (str.len var4))))
(assert (str.suffixof (str.replace var5 var4 var3) (str.at var4 var7)))
(check-sat)