(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (str.suffixof var0 var1))
(assert (str.prefixof (str.at var2 var3) (str.substr "wk" var4 var5)))
(assert (str.prefixof (str.substr (str.at var6 var7) (str.to.int var6) (str.len var0)) (str.at var6 var7)))
(assert (>= (str.to.int var1) (str.len var0)))
(check-sat)