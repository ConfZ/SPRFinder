(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (> (str.len (str.at var0 var1)) (str.indexof var2 var3 86)))
(assert (< var4 var5))
(assert (>= (str.indexof var6 var2 var7) (str.indexof var2 var6 var1)))
(assert (>= (str.to.int (str.substr var0 var5 var5)) (str.indexof var2 var2 var1)))
(check-sat)