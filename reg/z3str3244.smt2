(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (>= var0 var1))
(assert (str.suffixof (str.substr var2 var3 var4) (str.substr var5 69 var4)))
(assert (str.in.re var6 re.allchar))
(assert (< (str.indexof var7 var7 156) (str.to.int var5)))
(check-sat)