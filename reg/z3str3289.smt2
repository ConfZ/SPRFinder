(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(assert (<= (str.len var0) (str.indexof var1 var2 var3)))
(assert (str.in.re (str.replace var4 var2 var2) (re.* re.allchar)))
(assert (not (str.in.re var1 re.allchar)))
(assert (str.in.re (str.substr (str.at var4 var5) (str.len var0) (str.indexof var2 var4 var6)) (re.* re.allchar)))
(check-sat)