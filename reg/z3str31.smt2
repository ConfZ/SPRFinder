(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.prefixof (str.substr (str.replace var0 var1 var2) (str.len var3) (str.indexof var0 var1 var4)) (str.at var3 var5)))
(assert (> var6 var7))
(assert (> var4 55))
(assert (str.prefixof (str.replace var2 var0 var1) (str.replace (str.replace var1 var2 var0) (str.replace "#7x6dvs[\\" var3 var3) (str.at var3 15))))
(check-sat)