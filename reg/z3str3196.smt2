(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Int)
(assert (< (str.indexof var0 var1 var2) (str.indexof var3 var4 var5)))
(assert (str.in.re var3 re.allchar))
(assert (str.prefixof (str.at "}C&k6." var6) (str.substr (str.at var1 var7) (str.to.int var4) (str.len "%g%}Fz"))))
(assert (< var7 37))
(check-sat)