(set-logic QF_S)
(declare-fun var0 () Bool)
(declare-fun var1 () String)
(declare-fun var2 () Int)
(declare-fun var3 () String)
(declare-fun var4 () String)
(declare-fun var5 () Int)
(declare-fun var6 () Int)
(declare-fun var7 () String)
(declare-fun var8 () Int)
(assert (not var0))
(assert (str.contains (str.at (str.at var1 var2) (str.len var3)) (str.substr var4 var5 var6)))
(assert (str.contains (str.at var7 var8) (str.replace var7 var4 var1)))
(assert (str.in.re var4 re.allchar))
(check-sat)