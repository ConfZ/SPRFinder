(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () String)
(assert (str.contains (str.substr "*vu?b`YY;" var0 var1) (str.substr var2 var3 var4)))
(assert (str.contains (str.substr (str.replace var5 var6 var7) (str.indexof var2 var5 var0) (str.to.int "")) (str.substr var5 75 var0)))
(assert (>= (str.len "") (str.len "")))
(assert (<= var3 var0))
(check-sat)