(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(assert (<= (str.to.int var0) (str.to.int "DX""Dx>|aLR")))
(assert (str.in.re (str.replace var1 var2 var3) (re.* re.allchar)))
(assert (str.prefixof var0 var0))
(assert (str.in.re (str.substr (str.substr var3 var4 var5) (str.len var3) (str.len var1)) (re.+ re.allchar)))
(check-sat)