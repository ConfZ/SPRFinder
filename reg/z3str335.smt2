(set-logic QF_S)
(declare-fun var0 () Bool)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(declare-fun var8 () String)
(assert (not var0))
(assert (str.contains var1 var2))
(assert (not (< var3 var4)))
(assert (str.prefixof (str.substr var5 var6 var7) (str.replace var8 "UxkWv" "`eZn")))
(check-sat)