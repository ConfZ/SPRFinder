(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (<= (str.len var0) (str.indexof var1 var2 var3)))
(assert (not (str.suffixof (str.substr var4 var5 var6) (str.at var4 var7))))
(assert (> (str.indexof var0 var2 var6) (str.len var4)))
(assert (str.contains (str.replace var1 var1 var4) (str.replace var1 var0 var4)))
(check-sat)