(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () Int)
(declare-fun var4 () Int)
(declare-fun var5 () String)
(declare-fun var6 () String)
(declare-fun var7 () Int)
(assert (str.prefixof (str.at var0 var1) (str.substr var2 var3 var4)))
(assert (str.in.re (str.replace var5 "I^`MBdv" var6) (re.+ re.allchar)))
(assert (str.prefixof (str.at var6 71) (str.at var2 81)))
(assert (str.in.re (str.at var5 var7) (re.* re.allchar)))
(check-sat)