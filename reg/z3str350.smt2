(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (not (str.contains var0 var1)))
(assert (> (str.indexof var2 var3 var4) (str.indexof var3 var3 var5)))
(assert (str.prefixof (str.substr var0 var6 var7) (str.replace var1 var0 var3)))
(assert (str.prefixof (str.at var1 115) (str.from.int (str.indexof (str.substr var1 var6 var6) (str.at var0 var6) (str.len var2)))))
(check-sat)