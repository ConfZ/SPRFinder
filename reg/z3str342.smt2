(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(assert (str.suffixof var0 var1))
(assert (str.prefixof var2 var3))
(assert (>= 174 125))
(assert (str.suffixof (str.substr var2 var4 94) (str.substr var2 var5 var6)))
(check-sat)