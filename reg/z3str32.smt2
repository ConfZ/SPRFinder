(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.prefixof var0 "5^iKBe"))
(assert (< (str.to.int var1) (str.to.int var2)))
(assert (str.contains (str.substr "wg+kk(EnM'" var3 var4) (str.replace var5 var1 var2)))
(assert (str.suffixof (str.at "y$}L9;" var6) (str.substr var2 var7 var7)))
(check-sat)