(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () String)
(assert (str.contains (str.substr var0 var1 var2) (str.at var3 var4)))
(assert (str.suffixof (str.substr (str.substr var5 var6 var4) (str.to.int var7) (str.indexof var0 "RZk]CO{)," var4)) (str.at (str.replace var0 var5 var5) (str.to.int var0))))
(assert (> (str.len var7) (str.to.int var0)))
(assert (not (< var1 145)))
(check-sat)