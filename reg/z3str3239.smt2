(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (> var0 var1))
(assert (<= var2 var3))
(assert (> (str.indexof var4 var5 var2) (str.len var6)))
(assert (str.in.re var7 re.allchar))
(check-sat)