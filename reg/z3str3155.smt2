(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (> (str.len "|6ce&""pD;v") (str.to.int var0)))
(assert (str.contains (str.at var1 var2) (str.replace var3 var4 var4)))
(assert (>= 6 var5))
(assert (str.suffixof (str.at var1 89) (str.substr var4 var6 var7)))
(check-sat)