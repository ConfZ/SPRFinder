(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (>= (str.len var0) (str.indexof var1 var2 var3)))
(assert (> (str.len var4) (str.indexof (str.substr var0 var5 var6) (str.replace var1 var4 var0) (str.indexof "5" var0 var7))))
(assert (<= (str.len var2) (str.indexof "}Y" var1 var5)))
(assert (str.prefixof var2 var4))
(check-sat)