(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (> (str.to.int var0) (str.len var1)))
(assert (>= (str.len var2) (str.to.int var3)))
(assert (<= (str.len (str.substr var0 var4 var5)) (str.indexof var0 var2 var6)))
(assert (<= (str.indexof var3 var2 var7) (str.len var1)))
(check-sat)