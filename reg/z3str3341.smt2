(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () Int)
(declare-fun var4 () Bool)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () String)
(declare-fun var8 () String)
(assert (> var0 var1))
(assert (> var2 var3))
(assert (not var4))
(assert (str.suffixof (str.substr (str.at var5 65) (str.indexof var6 "l;m='J" var1) (str.len var7)) (str.at (str.replace var8 var6 var6) (str.to.int var8))))
(check-sat)