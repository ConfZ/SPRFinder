(set-logic QF_S)
(declare-fun var0 () String)
(declare-fun var1 () Int)
(declare-fun var2 () String)
(declare-fun var3 () String)
(declare-fun var4 () Int)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () Bool)
(assert (str.in.re (str.substr var0 var1 var1) (re.+ re.allchar)))
(assert (> (str.len var2) (str.len var3)))
(assert (str.suffixof (str.at "p?@%Q?Ik'F" var4) (str.substr "" var5 var6)))
(assert (not var7))
(check-sat)