(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (>= (str.to.int var0) (str.len var1)))
(assert (> var2 var3))
(assert (str.suffixof var4 "Yg"))
(assert (str.suffixof (str.at "1gv\\3}" var5) (str.substr var6 var7 var7)))
(check-sat)