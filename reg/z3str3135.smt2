(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(assert (<= (str.to.int (str.substr var0 var1 var2)) (str.len var3)))
(assert (>= var4 193))
(assert (str.in.re var5 re.allchar))
(assert (< var6 var1))
(check-sat)