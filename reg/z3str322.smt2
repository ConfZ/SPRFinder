(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (< var0 var1))
(assert (str.contains (str.replace "](>/%\\8-*s" var2 var3) (str.replace var4 var5 var5)))
(assert (str.suffixof (str.substr (str.at var4 var6) (str.indexof var2 var3 var7) (str.indexof var5 var3 var1)) (str.at var4 var6)))
(assert (str.suffixof (str.substr var4 var7 78) (str.substr "i3" var1 146)))
(check-sat)