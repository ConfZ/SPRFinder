(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.contains (str.at (str.substr var0 var1 49) (str.len var2)) (str.at (str.replace var3 var4 var2) (str.len var3))))
(assert (< (str.to.int var3) (str.indexof var2 var0 var5)))
(assert (str.contains var3 var3))
(assert (str.contains (str.replace (str.at var2 var6) (str.replace var4 var4 var0) (str.substr var0 var7 var1)) (str.replace var0 var0 var3)))
(check-sat)