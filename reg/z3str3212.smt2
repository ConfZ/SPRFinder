(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (> 81 var0))
(assert (<= (str.indexof var1 var2 var3) (str.len var4)))
(assert (str.in.re (str.substr var5 var6 var7) (re.+ re.allchar)))
(assert (< (str.to.int var5) (str.to.int var2)))
(check-sat)