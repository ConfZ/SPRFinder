(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(assert (str.contains var0 var1))
(assert (>= (str.to.int var2) (str.len (str.at "D,_s" 112))))
(assert (str.contains var3 var1))
(assert (>= (str.len (str.replace var3 var1 var3)) (str.indexof var0 "/" var4)))
(check-sat)