(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (>= (str.to.int var0) (str.len var1)))
(assert (<= (str.indexof var2 var3 var4) (str.indexof var0 var1 13)))
(assert (>= var5 var6))
(assert (>= (str.len (str.substr var2 var7 var6)) (str.indexof (str.substr "sn~d);*u" var7 var6) (str.substr "+^?" 15 var5) (str.indexof var1 var0 var6))))
(check-sat)