(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (>= (str.len var0) (str.to.int var1)))
(assert (not (<= var2 79)))
(assert (str.prefixof (str.substr var3 var4 var5) (str.replace "" var6 var0)))
(assert (>= (str.to.int var1) (str.indexof var6 var1 var7)))
(check-sat)