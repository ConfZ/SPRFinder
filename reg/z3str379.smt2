(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(assert (str.in.re (str.at (str.replace var0 var1 var2) (str.to.int var3)) (re.* re.allchar)))
(assert (< (str.to.int var3) (str.len var1)))
(assert (>= (str.indexof var0 var2 var4) (str.len var0)))
(assert (>= var5 var6))
(check-sat)