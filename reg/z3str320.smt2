(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Bool)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(declare-fun var8 () Int)
(assert (not (str.contains var0 var1)))
(assert (not var2))
(assert (str.in.re var3 re.allchar))
(assert (>= (str.len (str.substr var4 var5 var6)) (str.len (str.substr var1 var7 var8))))
(check-sat)