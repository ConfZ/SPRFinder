(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (<= (str.to.int var0) (str.to.int (str.replace var1 var2 var3))))
(assert (str.in.re (str.replace "ktA;""" var0 var0) (re.* re.allchar)))
(assert (str.prefixof (str.substr var2 var4 var5) (str.replace var3 var2 var0)))
(assert (< var6 var7))
(check-sat)