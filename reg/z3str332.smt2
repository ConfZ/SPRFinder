(set-logic QF_S)
(declare-fun var0 () Int)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () Int)
(declare-fun var4 () String)
(declare-fun var5 () String)
(declare-fun var6 () Int)
(declare-fun var7 () String)
(assert (str.suffixof (str.at "^C$Kx" var0) (str.substr var1 var2 var3)))
(assert (> (str.len var4) (str.to.int "lR~`zT@F78")))
(assert (str.in.re (str.substr var7 var6 var2) (re.+ re.allchar)))
(assert (str.suffixof (str.substr var5 var2 var3) (str.at var4 65)))
(check-sat)