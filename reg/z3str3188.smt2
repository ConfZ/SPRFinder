(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (str.in.re (str.substr var0 var1 var2) (re.* re.allchar)))
(assert (not (str.contains var3 var4)))
(assert (str.suffixof (str.substr var5 var6 var7) (str.substr var3 142 var6)))
(assert (str.suffixof ".d" var0))
(check-sat)