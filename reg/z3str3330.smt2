(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (str.in.re var0 re.allchar))
(assert (> var1 var2))
(assert (str.suffixof (str.substr var3 var4 var5) (str.replace (str.substr var6 var5 var2) (str.at var7 var4) (str.at var0 var2))))
(assert (str.suffixof (str.substr var7 var1 var4) (str.at var0 var4)))
(check-sat)