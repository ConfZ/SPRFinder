(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (> var0 var1))
(assert (str.in.re (str.replace (str.substr var2 78 var3) (str.replace var4 var5 var6) (str.at var5 var7)) (re.* (re.* re.allchar))))
(assert (str.contains var4 "'~6b"))
(assert (<= (str.len (str.substr var6 var0 var1)) (str.indexof (str.at "n" var1) (str.replace var5 var6 var2) (str.indexof var4 var4 var7))))
(check-sat)