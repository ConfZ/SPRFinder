(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(declare-fun var8 () Bool)
(assert (str.contains (str.substr (str.substr var0 var1 var2) (str.indexof var3 var4 41) (str.indexof var5 var5 var6)) (str.at (str.replace var0 var0 var4) (str.len var4))))
(assert (str.in.re (str.substr var3 var7 var6) (re.+ re.allchar)))
(assert (not (not var8)))
(assert (not (> var6 var2)))
(check-sat)