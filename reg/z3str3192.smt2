(set-logic QF_S)
(declare-fun var0 () Bool)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () String)
(declare-fun var8 () String)
(assert (not var0))
(assert (str.suffixof (str.at var1 var2) (str.substr "'a$V" var3 var4)))
(assert (str.contains (str.at (str.at var5 var6) (str.to.int var7)) (str.at (str.substr var8 var2 var4) (str.indexof var8 var8 var2))))
(assert (>= (str.to.int var7) (str.to.int "S\\[{c+-'")))
(check-sat)