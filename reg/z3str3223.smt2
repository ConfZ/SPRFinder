(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () String)
(assert (not (>= var0 var1)))
(assert (str.contains (str.substr (str.at var2 var3) (str.indexof var4 var5 var6) (str.to.int var7)) (str.substr var7 var0 var6)))
(assert (> var6 var0))
(assert (> (str.len var5) (str.to.int var2)))
(check-sat)