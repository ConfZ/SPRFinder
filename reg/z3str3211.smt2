(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (str.suffixof (str.substr "*+" var0 var1) (str.substr var2 var3 var4)))
(assert (< (str.indexof (str.substr var5 var4 var1) (str.at var6 var1) (str.len var7)) (str.len (str.substr var2 var4 var1))))
(assert (str.contains var5 var6))
(assert (str.prefixof "o@H" var7))
(check-sat)