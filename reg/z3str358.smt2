(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Bool)
(declare-fun var7 () String)
(declare-fun var8 () Int)
(assert (<= (str.to.int var0) (str.indexof var1 var2 var3)))
(assert (not (>= var4 var5)))
(assert (not (not var6)))
(assert (<= (str.to.int var7) (str.to.int (str.at var1 var8))))
(check-sat)